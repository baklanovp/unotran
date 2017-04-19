program test_sweeper
use material, only : create_material, number_legendre, number_groups
  use angle, only : initialize_angle, p_leg, number_angles, initialize_polynomials
  use mesh, only : create_mesh, number_cells
  use state, only : initialize_state, phi, source, psi
  use sweeper, only : sweep
  implicit none
  
  ! initialize types
  integer :: fineMesh(3), materialMap(3), l, c, a, g, counter, testCond, t1, t2
  double precision :: courseMesh(4), norm, error, phi_test(7,28)
  
  ! Define problem parameters
  character(len=17) :: filename = 'test/testXS.anlxs'
  fineMesh = [3, 22, 3]
  materialMap = [6,1,6]
  courseMesh = [0.0, 0.09, 1.17, 1.26]
  
  ! Make the mesh
  call create_mesh(fineMesh, courseMesh, materialMap)
  
  ! Read the material cross sections
  call create_material(filename)
  
  ! Create the cosines and angle space
  call initialize_angle(10, 1)
  ! Create the set of polynomials used for the anisotropic expansion
  call initialize_polynomials(number_legendre)
    
  ! Create the state variable containers
  call initialize_state()

  source = 1.0

  error = 1.0
  norm = 0.0
  counter = 1
  do while (error .gt. 1e-12)
    call sweep()
    error = abs(norm - norm2(phi))
    norm = norm2(phi)
    counter = counter + 1
  end do
  
  phi_test = reshape((/ 2.43576516357,  4.58369841267,  1.5626711117,  1.31245374786,  1.12046360588,  &
                        0.867236739559,  0.595606769942,  2.47769600029,  4.77942918468,  1.71039214967,  &
                        1.45482285016,  1.2432932006,  1.00395695756,  0.752760077886,  2.51693149995,  &
                        4.97587877605,  1.84928362206,  1.58461198915,  1.35194171606,  1.11805871638,  &
                        0.810409774028,  2.59320903064,  5.23311939144,  1.97104981208,  1.69430758654,  &
                        1.44165108478,  1.20037776749,  0.813247000713,  2.70124816247,  5.52967658354,  &
                        2.07046672497,  1.78060787735,  1.51140559905,  1.25273492166,  0.808917503514,  &
                        2.79641531407,  5.78666661987,  2.15462056117,  1.85286457556,  1.56944290225,  &
                        1.29575568046,  0.813378868173,  2.87941186529,  6.00774402332,  2.22561326404,  &
                        1.91334927054,  1.61778278393,  1.33135223233,  0.819884638625,  2.95082917982,  &
                        6.19580198153,  2.28505426287,  1.96372778133,  1.65788876716,  1.36080630864,  &
                        0.82640046716,  3.01116590643,  6.35316815516,  2.3341740765,  2.00522071328,  &
                        1.69082169384,  1.38498482157,  0.83227605712,  3.06083711902,  6.48170764214,  &
                        2.37390755792,  2.0387192711,  1.71734879522,  1.40447856797,  0.837283759523,  &
                        3.10018046121,  6.58289016281,  2.40495581492,  2.06486841143,  1.73802084073,  &
                        1.4196914264,  0.841334574174,  3.12946077671,  6.6578387922,  2.4278320614,  &
                        2.08412599358,  1.75322625595,  1.43089755336,  0.844390210178,  3.14887366178,  &
                        6.70736606465,  2.44289487705,  2.09680407626,  1.76322843396,  1.43827772036,  &
                        0.846433375617,  3.15854807829,  6.73199979835,  2.4503712844,  2.10309664539,  &
                        1.76819052183,  1.44194181402,  0.847456401368,  3.15854807829,  6.73199979835,  &
                        2.4503712844,  2.10309664539,  1.76819052183,  1.44194181402,  0.847456401368,  &
                        3.14887366178,  6.70736606465,  2.44289487705,  2.09680407626,  1.76322843396,  &
                        1.43827772036,  0.846433375617,  3.12946077671,  6.6578387922,  2.4278320614,  &
                        2.08412599358,  1.75322625595,  1.43089755336,  0.844390210178,  3.10018046121,  &
                        6.58289016281,  2.40495581492,  2.06486841143,  1.73802084073,  1.4196914264,  &
                        0.841334574174,  3.06083711902,  6.48170764214,  2.37390755792,  2.0387192711,  &
                        1.71734879522,  1.40447856797,  0.837283759523,  3.01116590643,  6.35316815516,  &
                        2.3341740765,  2.00522071328,  1.69082169384,  1.38498482157,  0.83227605712,  &
                        2.95082917982,  6.19580198153,  2.28505426287,  1.96372778133,  1.65788876716,  &
                        1.36080630864,  0.82640046716,  2.87941186529,  6.00774402332,  2.22561326404,  &
                        1.91334927054,  1.61778278393,  1.33135223233,  0.819884638625,  2.79641531407,  &
                        5.78666661987,  2.15462056117,  1.85286457556,  1.56944290225,  1.29575568046,  &
                        0.813378868173,  2.70124816247,  5.52967658354,  2.07046672497,  1.78060787735,  &
                        1.51140559905,  1.25273492166,  0.808917503514,  2.59320903064,  5.23311939144,  &
                        1.97104981208,  1.69430758654,  1.44165108478,  1.20037776749,  0.813247000713,  &
                        2.51693149995,  4.97587877605,  1.84928362206,  1.58461198915,  1.35194171606,  &
                        1.11805871638,  0.810409774028,  2.47769600029,  4.77942918468,  1.71039214967,  &
                        1.45482285016,  1.2432932006,  1.00395695756,  0.752760077886,  2.43576516357,  &
                        4.58369841267,  1.5626711117,  1.31245374786,  1.12046360588,  0.867236739559,  &
                        0.595606769942 /),shape(phi_test))
                 
  t1 = testCond(norm2(phi(0,:,:) - phi_test) .lt. 2e-5)
  
  if (t1 .eq. 0) then
    print *, 'main: phi comparison failed'
  else
    print *, 'all tests passed for main'
  end if

end program test_sweeper

integer function testCond(condition)
  logical, intent(in) :: condition
  if (condition) then
    write(*,"(A)",advance="no") '.'
    testCond = 1
  else
    write(*,"(A)",advance="no") 'F'
    testCond = 0
  end if

end function testCond