module sweeper

  implicit none
  
  contains
  
  subroutine sweep(phi, psi, incident)
    ! ##########################################################################
    ! Sweep over each cell, angle, and octant
    ! ##########################################################################

    ! Use Statements
    use angle, only : p_leg, wt, mu
    use mesh, only : dx
    use control, only : store_psi, boundary_type, number_angles, number_cells, &
                        number_legendre, number_groups
    use state, only : mg_sig_t, sweep_count, mg_mMap
    use sources, only : compute_within_group_source, compute_in_source

    ! Variable definitions
    double precision, intent(inout), dimension(:,:,:) :: &
        phi,      & ! Scalar flux for current iteration and group g
        psi         ! Angular flux for current iteration and group g
    double precision, intent(inout), dimension(:,:) :: &
        incident    ! Angular flux incident on the cell in group g
    integer :: &
        g,          & ! Group index
        o,          & ! Octant index
        c,          & ! Cell index
        mat,        & ! Material index
        a,          & ! Angle index
        an,         & ! Global angle index
        cmin,       & ! Lower cell number
        cmax,       & ! Upper cell number
        cstep,      & ! Cell stepping direction
        amin,       & ! Lower angle number
        amax,       & ! Upper angle number
        astep         ! Angle stepping direction
    double precision, dimension(0:number_legendre) :: &
        M           ! Legendre polynomial integration vector
    double precision :: &
        psi_center, & ! Angular flux at cell center
        source        ! Fission, In-Scattering, External source in group g
    logical :: &
        octant        ! Positive/Negative octant flag

    ! Compute the into group sources for group g
    call compute_in_source()

    ! Increment the sweep counter
    sweep_count = sweep_count + 1

    ! Reset phi
    phi = 0.0

    do o = 1, 2  ! Sweep over octants
      ! Sweep in the correct direction within the octant
      octant = o == 1
      amin = merge(1, number_angles, octant)
      amax = merge(number_angles, 1, octant)
      astep = merge(1, -1, octant)
      cmin = merge(1, number_cells, octant)
      cmax = merge(number_cells, 1, octant)
      cstep = merge(1, -1, octant)

      ! set boundary conditions
      incident = boundary_type(o) * incident  ! Set albedo conditions

      do c = cmin, cmax, cstep  ! Sweep over cells
        do a = amin, amax, astep  ! Sweep over angle
          ! Get the correct angle index
          an = merge(a, 2 * number_angles - a + 1, octant)

          ! legendre polynomial integration vector
          M = wt(a) * p_leg(:, an)

          ! Loop over the energy groups
          do g = 1, number_groups

            mat = mg_mMap(c)

            ! Get the source in this cell, group, and angle
            source = compute_within_group_source(g, c, an)

            ! Use the specified equation.  Defaults to DD
            call computeEQ(source, incident(g, a), mg_sig_t(g, mat), dx(c), mu(a), psi_center)

            if (store_psi) then
              psi(g, an, c) = psi_center
            end if

            ! Increment the legendre expansions of the scalar flux
            phi(:, g, c) = phi(:, g, c) + M(:) * psi_center
          end do
        end do
      end do
    end do

  end subroutine sweep
  
  subroutine computeEQ(S, incident, sig, dx, mua, cellPsi)
    ! ##########################################################################
    ! Compute the value for the closure relationship
    ! ##########################################################################

    ! Use statements
    use control, only : equation_type

    ! Variable definitions
    double precision, intent(inout) :: &
        incident ! Angular flux incident on the cell
    double precision, intent(in) :: &
        S,     & ! Source within the cell
        sig,   & ! Total cross section within the cell
        dx,    & ! Width of the cell
        mua      ! Angle for the cell
    double precision, intent(out) :: &
        cellPsi  ! Angular flux at cell center
    double precision :: &
        tau,   & ! Parameter used in step characteristics
        A,     & ! Parameter used in step characteristics
        invmu    ! Parameter used in diamond and step differences

    select case (equation_type)
    case ('DD')
      ! Diamond Difference relationship
      invmu = dx / (2 * abs(mua))
      cellPsi = (incident + invmu * S) / (1 + invmu * sig)
      incident = 2 * cellPsi - incident
    case ('SC')
      ! Step Characteristics relationship
      tau = sig * dx / mua
      A = exp(-tau)
      cellPsi = incident * (1.0 - A) / tau + S * (sig * dx + mua * (A - 1.0)) / (sig ** 2 * dx)
      incident = A * incident + S * (1.0 - A) / sig
    case ('SD')
      ! Step Difference relationship
      invmu = dx / (abs(mua))
      cellPsi = (incident + invmu * S) / (1 + invmu * sig)
      incident = cellPsi
    case default
      print *, 'ERROR : Equation not implemented'
    end select
  
  end subroutine computeEQ
  
end module sweeper
