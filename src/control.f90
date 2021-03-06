module control
  ! ############################################################################
  ! Define the options for solving the transport equation
  ! ############################################################################

  implicit none

  ! control variables
  integer, parameter :: dp = selected_real_kind(15, 307)
  real(kind=dp), allocatable, dimension(:) :: &
      coarse_mesh,                & ! Coarse mesh boundaries
      coarse_mesh_x,              & ! Coarse mesh boundaries in x direction
      coarse_mesh_y                 ! Coarse mesh boundaries in y direction
  integer, allocatable, dimension(:) :: &
      fine_mesh,                  & ! Number of fine cells per coarse region
      fine_mesh_x,                & ! Number of fine cells per coarse region in x direction
      fine_mesh_y,                & ! Number of fine cells per coarse region in y direction
      material_map,               & ! Material ID within each coarse region
      energy_group_map,           & ! Coarse energy group boundaries
      truncation_map,             & ! Expansion order within each coarse group (optional)
      homogenization_map            ! Map of which fine cells to homogenize for DGM (optional)
  real(kind=dp) :: &
      boundary_east,              & ! Albedo value at east boundary
      boundary_west,              & ! Albedo value at west boundary
      boundary_north,             & ! Albedo value at north boundary
      boundary_south,             & ! Albedo value at south boundary
      recon_tolerance=1e-8_8,     & ! Convergance criteria for recon iteration
      eigen_tolerance=1e-8_8,     & ! Convergance criteria for eigen iteration
      outer_tolerance=1e-8_8,     & ! Convergance criteria for outer iteration
      lamb=1.0_8,                 & ! Parameter (0 < lamb <= 1.0) for krasnoselskii iteration
      source_value=0.0_8,         & ! Value of external source for the problem
      initial_keff=1.0_8            ! Initial value for the eigenvalue
  character(len=256) :: &
      xs_name,                    & ! Name of the cross section file
      dgm_basis_name,             & ! Name of file containing energy basis
      file_name,                  & ! Name of file containing the options
      initial_phi,                & ! Name of file with initial scalar flux
      initial_psi,                & ! Name of file with initial angular flux
      solver_type                   ! Choice of [eigen, fixed] solver
  character(len=2) :: &
      equation_type="DD"            ! Closure equation for discrete ordinates [DD, SC, SD]
  integer :: &
      spatial_dimension,          & ! Dimension of the spatial variable (1 for 1D, 2 for 2D)
      angle_order,                & ! Number of angles per octant
      angle_option,               & ! Quadrature option [gl=0, dgl=1]
      max_recon_iters=1000,       & ! Maximum iterations for recon loop
      max_eigen_iters=1000,       & ! Maximum iterations for eigen loop
      max_outer_iters=1000,       & ! Maximum iterations for outer loop
      min_recon_iters=1,          & ! Minimum iterations for recon loop
      min_eigen_iters=1,          & ! Minimum iterations for eigen loop
      min_outer_iters=1,          & ! Minimum iterations for outer loop
      number_cells_x,             & ! Total number of spatial cells in the x direction
      number_cells_y,             & ! Total number of spatial cells in the y direction
      number_cells,               & ! Total number of spatial cells in the mesh
      number_regions,             & ! Number of unique material regions
      number_angles_per_octant,   & ! Number of angles per octant (half space in 1D, quadrant in 2D)
      number_angles,              & ! Total number of angles
      number_groups,              & ! Number of groups for the MG problem
      number_fine_groups,         & ! Number of groups in the cross section library
      number_coarse_groups,       & ! Number of groups in the expansion
      number_legendre,            & ! Number of anisotropic scattering orders
      number_moments,             & ! Total number of legendre moments (equal to number_legendre in 1D)
      recon_print=1,              & ! Enable/Disable recon iteration printing
      eigen_print=1,              & ! Enable/Disable eigen iteration printing
      outer_print=1,              & ! Enable/Disable outer iteration printing
      store_phi_order=-1,         & ! Legendre order for storage of the scalar flux moments
      scatter_leg_order=-1,       & ! Legendre order for anisotropic scattering
      delta_leg_order=-1            ! Legendre order for truncated expansion of delta term
  logical :: &
      allow_fission=.false.,      & ! Enable/Disable fission in the problem
      allow_scatter=.true.,       & ! Enable/Disable scattering in the problem
      use_dgm=.false.,            & ! Enable/Disable DGM solver
      store_psi=.false.,          & ! Enable/Disable storing the angular flux
      ignore_warnings=.true.,     & ! Enable/Disable warning messages
      outer_converged=.false.,    & ! Flag to state if the outer iterations have converged
      eigen_converged=.false.,    & ! Flag to state if the eigen iterations have converged
      truncate_delta=.false.,     & ! Enable/Disable truncated expansion of delta term
      verify_control=.true.         ! Enable/Disable checking control variables

  contains

  subroutine initialize_control(fname, silent)
    ! ##########################################################################
    ! Read the options file and output the choices if not silent
    ! ##########################################################################

    ! Input variables
    character(len=524288) :: &
        buffer, & ! Buffer to hold read-in strings
        label     ! Contains the read-variable name
    character(len=*), intent(in) :: &
        fname     ! Name of the file containing options
    integer :: &
        pos,    & ! Position indicator in the line
        ios=0,  & ! I/O file flag
        line=0    ! Line number
    integer, parameter :: &
        fh=15     ! File number
    logical, optional :: &
        silent    ! Flag to prevent printing the read variables and values
    logical :: &
        no_print  ! Local flag to prevent printing the read variables and values

    ! Set the local value of no_print from silent
    if (present(silent)) then
      no_print = silent   ! Use provided value
    else
      no_print = .false.  ! Default value
    end if

    ! Cut the trailing whitespace from fname
    file_name = trim(adjustl(fname))

    ! Start reading the options file
    open(fh, file=file_name, action='read', iostat=ios)
    if (ios > 0) stop "*** ERROR: user input file not found ***"

    ! ios is negative if an end of record condition is encountered or if
    ! an endfile condition was detected.  It is positive if an error was
    ! detected.  ios is zero otherwise.
    do while (ios == 0)
      read(fh, '(A)', iostat=ios) buffer
      if (ios == 0) then
        ! Increment the line count
        line = line + 1

        ! Find the first whitespace and split label and data
        pos = scan(buffer, ' ')
        label = buffer(1:pos)
        buffer = buffer(pos+1:)

        ! Parse the label and save the value to the proper variable
        select case (label)
        case ('fine_mesh')
          allocate(fine_mesh(nitems(buffer)))
          read(buffer, *, iostat=ios) fine_mesh
        case ('coarse_mesh')
          allocate(coarse_mesh(nitems(buffer)))
          read(buffer, *, iostat=ios) coarse_mesh
        case ('fine_mesh_x')
          allocate(fine_mesh_x(nitems(buffer)))
          read(buffer, *, iostat=ios) fine_mesh_x
        case ('fine_mesh_y')
          allocate(fine_mesh_y(nitems(buffer)))
          read(buffer, *, iostat=ios) fine_mesh_y
        case ('coarse_mesh_x')
          allocate(coarse_mesh_x(nitems(buffer)))
          read(buffer, *, iostat=ios) coarse_mesh_x
        case ('coarse_mesh_y')
          allocate(coarse_mesh_y(nitems(buffer)))
          read(buffer, *, iostat=ios) coarse_mesh_y
        case ('material_map')
          allocate(material_map(nitems(buffer)))
          read(buffer, *, iostat=ios) material_map
        case ('homogenization_map')
          allocate(homogenization_map(nitems(buffer)))
          read(buffer, *, iostat=ios) homogenization_map
        case ('xs_file')
          xs_name=trim(adjustl(buffer))
        case ('initial_phi')
          initial_phi=trim(adjustl(buffer))
        case ('initial_psi')
          initial_psi=trim(adjustl(buffer))
        case ('initial_keff')
          read(buffer, *, iostat=ios) initial_keff
        case ('angle_order')
          read(buffer, *, iostat=ios) angle_order
        case ('angle_option')
          read(buffer, *, iostat=ios) angle_option
        case ('boundary_east')
          read(buffer, *, iostat=ios) boundary_east
        case ('boundary_west')
          read(buffer, *, iostat=ios) boundary_west
        case ('boundary_north')
          read(buffer, *, iostat=ios) boundary_north
        case ('boundary_south')
          read(buffer, *, iostat=ios) boundary_south
        case ('allow_fission')
          read(buffer, *, iostat=ios) allow_fission
        case ('energy_group_map')
          allocate(energy_group_map(nitems(buffer)))
          read(buffer, *, iostat=ios) energy_group_map
        case ('dgm_basis_file')
          dgm_basis_name=trim(adjustl(buffer))
        case ('truncation_map')
          allocate(truncation_map(nitems(buffer)))
          read(buffer, *, iostat=ios) truncation_map
        case ('recon_print')
          read(buffer, *, iostat=ios) recon_print
        case ('eigen_print')
          read(buffer, *, iostat=ios) eigen_print
        case ('outer_print')
          read(buffer, *, iostat=ios) outer_print
        case ('recon_tolerance')
          read(buffer, *, iostat=ios) recon_tolerance
        case ('eigen_tolerance')
          read(buffer, *, iostat=ios) eigen_tolerance
        case ('outer_tolerance')
          read(buffer, *, iostat=ios) outer_tolerance
        case ('lambda')
          read(buffer, *, iostat=ios) lamb
        case ('use_DGM')
          read(buffer, *, iostat=ios) use_DGM
        case ('store_psi')
          read(buffer, *, iostat=ios) store_psi
        case ('ignore_warnings')
          read(buffer, *, iostat=ios) ignore_warnings
        case ('equation_type')
          equation_type=trim(adjustl(buffer))
        case ('solver_type')
          solver_type=trim(adjustl(buffer))
        case ('source')
          read(buffer, *, iostat=ios) source_value
        case ('scatter_legendre_order')
          read(buffer, *, iostat=ios) scatter_leg_order
        case ('delta_legendre_order')
          read(buffer, *, iostat=ios) delta_leg_order
        case ('truncate_delta')
          read(buffer, *, iostat=ios) truncate_delta
        case ('max_recon_iters')
          read(buffer, *, iostat=ios) max_recon_iters
        case ('max_eigen_iters')
          read(buffer, *, iostat=ios) max_eigen_iters
        case ('max_outer_iters')
          read(buffer, *, iostat=ios) max_outer_iters
        case ('spatial_dimension')
          read(buffer, *, iostat=ios) spatial_dimension
        case default
          print *, 'Skipping invalid label at line', line
        end select
      end if
    end do
    close(fh)

    ! If DGM is enabled, angular flux must be stored
    if (use_DGM) then
      store_psi = .true.
    end if

    ! Unless disabled, send the options to standard output
    if (.not. no_print) then
      call output_control()
    end if

  end subroutine initialize_control

  subroutine output_control()
    ! ##########################################################################
    ! Output the variables/options to the standard output
    ! ##########################################################################

    print *, 'MESH VARIABLES'
    print *, '  spatial_dimension  = [', spatial_dimension, ']'
    print *, '  fine_mesh_x        = [', fine_mesh_x, ']'
    if (spatial_dimension == 2) then
      print *, '  fine_mesh_y        = [', fine_mesh_y, ']'
    end if
    print *, '  coarse_mesh_x      = [', coarse_mesh_x, ']'
    if (spatial_dimension == 2) then
      print *, '  coarse_mesh_y      = [', coarse_mesh_y, ']'
    end if
    print *, '  material_map       = [', material_map, ']'
    print *, '  boundary_east      = [', boundary_east, ']'
    print *, '  boundary_west      = [', boundary_west, ']'
    if (spatial_dimension == 2) then
      print *, '  boundary_north      = [', boundary_north, ']'
      print *, '  boundary_south      = [', boundary_south, ']'
    end if
    print *, 'MATERIAL VARIABLES'
    print *, '  xs_file_name       = "', trim(xs_name), '"'
    print *, 'ANGLE VARIABLES'
    print *, '  angle_option       = ', angle_option
    print *, 'SOURCE'
    print *, '  constant source    = ', source_value
    print *, 'OPTIONS'
    print *, '  initial_phi        = ', trim(initial_phi)
    print *, '  initial_psi        = ', trim(initial_psi)
    print *, '  initial_keff       = ', initial_keff
    print *, '  solver_type        = "', trim(solver_type), '"'
    print *, '  equation_type      = "', trim(equation_type), '"'
    print *, '  store_psi          = ', store_psi
    print *, '  allow_fission      = ', allow_fission
    if (solver_type == 'eigen') then
      print *, '  eigen_print        = ', eigen_print
      print *, '  eigen_tolerance    = ', eigen_tolerance
      print *, '  max_eigen_iters    = ', max_eigen_iters
    end if
    print *, '  outer_print        = ', outer_print
    print *, '  outer_tolerance    = ', outer_tolerance
    print *, '  max_outer_iters    = ', max_outer_iters
    print *, '  lambda             = ', lamb
    print *, '  ignore_warnings    = ', ignore_warnings
    if (scatter_leg_order > -1) then
      print *, '  scatter_order      = ', scatter_leg_order
    else
      print *, '  scatter_order     = DEFAULT'
    end if
    if (use_DGM) then
      print *, 'DGM OPTIONS'
      print *, '  dgm_basis_file     = "', trim(dgm_basis_name), '"'
      print *, '  use_DGM            = ', use_DGM
      print *, '  recon_print        = ', recon_print
      print *, '  recon_tolerance    = ', recon_tolerance
      print *, '  max_recon_iters    = ', max_recon_iters
      if (allocated(energy_group_map)) then
        print *, '  energy_group_map   = [', energy_group_map, ']'
      end if
      if (allocated(truncation_map)) then
        print *, '  truncation_map     = [', truncation_map, ']'
      end if
      if (allocated(homogenization_map)) then
        print *, '  homogenization_map = [', homogenization_map, ']'
      end if
    else
      print *, '  use_dgm            = ', use_dgm
    end if

  end subroutine output_control

  subroutine check_inputs()
    ! ##########################################################################
    ! Verify the inputs are defined correctly
    ! ##########################################################################

    ! Check spatial dimension
    if (.not. (spatial_dimension == 1 .or. spatial_dimension == 2)) then
      print *, 'INPUT ERROR : Invalid spatial dimension [', spatial_dimension, '] selected.  Only 1D and 2D supported'
      stop
    end if

    ! Check solver type
    if (.not. (solver_type == 'eigen' .or. solver_type == 'fixed')) then
      print *, 'INPUT ERROR : Invalid solver type'
      stop
    end if

    ! Check that the homogenization_map is provided correctly
    if (allocated(homogenization_map)) then
      if (spatial_dimension == 1) then
        if (sum(fine_mesh_x) /= size(homogenization_map)) then
          print *, 'INPUT ERROR : homogenization map is the wrong size'
          stop
        end if
      else
        if (sum(fine_mesh_x) * sum(fine_mesh_y) /= size(homogenization_map)) then
          print *, 'INPUT ERROR : homogenization map is the wrong size'
          stop
        end if
      end if
      if (minval(homogenization_map) /= 1) then
        print *, 'INPUT ERROR : the first homogenization cell should be designated as 1'
        stop
      end if
    end if

    ! Check that the energy_group_map is provided correctly
    if (allocated(energy_group_map)) then
      if (size(energy_group_map) /= number_fine_groups) then
        print *, size(energy_group_map), number_fine_groups
        print *, 'INPUT ERROR : energy group map must have a coarse group for all fine groups'
        stop
      end if
      if (minval(energy_group_map) /= 1) then
        print *, 'INPUT ERROR : the first energy group mapping should be designated as 1'
        stop
      end if
    end if

  end subroutine check_inputs

  subroutine finalize_control()
    ! ##########################################################################
    ! Deallocate all allocated arrays
    ! ##########################################################################

    if (allocated(fine_mesh)) then
      deallocate(fine_mesh)
    end if
    if (allocated(fine_mesh_x)) then
      deallocate(fine_mesh_x)
    end if
    if (allocated(fine_mesh_y)) then
      deallocate(fine_mesh_y)
    end if
    if (allocated(coarse_mesh)) then
      deallocate(coarse_mesh)
    end if
    if (allocated(coarse_mesh_x)) then
      deallocate(coarse_mesh_x)
    end if
    if (allocated(coarse_mesh_y)) then
      deallocate(coarse_mesh_y)
    end if
    if (allocated(material_map)) then
      deallocate(material_map)
    end if
    if (allocated(energy_group_map)) then
      deallocate(energy_group_map)
    end if
    if (allocated(truncation_map)) then
      deallocate(truncation_map)
    end if
    if (allocated(homogenization_map)) then
      deallocate(homogenization_map)
    end if
  end subroutine finalize_control

  ! Copied from http://www.tek-tips.com/viewthread.cfm?qid=1688013
  ! Credit to salgerman
  integer function nitems(line)
    ! ##########################################################################
    ! Compute the number of space-separated items in a line
    ! ##########################################################################

    character line*(*)
    logical back
    integer length, k

    back = .true.
    length = len_trim(line)
    k = index(line(1:length), ' ', back)
    if (k == 0) then
      nitems = 0
      return
    end if

    nitems = 1
    do
      ! starting with the right most blank space,
      ! look for the next non-space character down
      ! indicating there is another item in the line
      do
        if (k <= 0) exit
        if (line(k:k) == ' ') then
          k = k - 1
          cycle
        else
          nitems = nitems + 1
          exit
        end if
      end do

      ! once a non-space character is found,
      ! skip all adjacent non-space character
      do
        if ( k<=0 ) exit
        if (line(k:k) /= ' ') then
          k = k - 1
          cycle
        end if
        exit
      end do
      if (k <= 0) exit
    end do
  end function nitems

end module control
