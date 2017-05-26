module solver
  use control, only : lambda, outer_print, outer_tolerance, store_psi
  use material, only : create_material, number_legendre, number_groups, finalize_material, &
                       sig_t, sig_s, nu_sig_f, chi
  use angle, only : initialize_angle, p_leg, number_angles, initialize_polynomials, finalize_angle
  use mesh, only : create_mesh, number_cells, finalize_mesh
  use state, only : initialize_state, phi, psi, source, finalize_state
  use sweeper, only : sweep

  implicit none
  
  logical :: printOption, use_fission
  double precision, allocatable :: incoming(:,:)

  contains
  
  ! Initialize all of the variables and solvers
  subroutine initialize_solver()
    ! initialize the mesh
    call create_mesh()
    ! read the material cross sections
    call create_material()
    ! initialize the angle quadrature
    call initialize_angle()
    ! get the basis vectors
    call initialize_polynomials(number_legendre)
    ! allocate the solutions variables
    call initialize_state()

    allocate(incoming(number_groups, number_angles * 2))
    incoming = 0.0

  end subroutine initialize_solver

  ! Interate equations until convergance
  subroutine solve()
    ! Inputs
    !   eps : error tolerance for convergance
    !   lambda_arg (optional) : value of lambda for Krasnoselskii iteration

    double precision :: norm, error, hold
    integer :: counter

    ! Error of current iteration
    error = 1.0
    ! 2 norm of the scalar flux
    norm = norm2(phi)
    ! interation number
    counter = 1
    do while (error > outer_tolerance)  ! Interate to convergance tolerance
      ! Sweep through the mesh
      call sweep(phi, psi, incoming)
      ! Store norm of scalar flux
      hold = norm2(phi)
      ! error is the difference in the norm of phi for successive iterations
      error = abs(norm - hold)
      ! Keep the norm for the next iteration
      norm = hold
      ! output the current error and iteration number
      if (outer_print) then
        print *, error, counter
      end if
      ! increment the iteration
      counter = counter + 1
    end do

  end subroutine solve

  subroutine output()

    ! output the resulting scalar flux
    print *, phi(0,:,:)
    ! output angular flux
    if (store_psi) then
      print *
      print *, psi(:,:,:)
    end if

  end subroutine output

  subroutine finalize_solver()
    call finalize_angle()
    call finalize_mesh()
    call finalize_material()
    call finalize_state()
    if (allocated(incoming)) then
      deallocate(incoming)
    end if
  end subroutine

end module solver
