import sys
from numpy.ma.testutils import assert_almost_equal
sys.path.append('../')

import unittest
import pydgm
import numpy as np


class TestDGMSOLVER(unittest.TestCase):

    def setUp(self):
        # Set the variables for the test
        pydgm.control.spatial_dimension = 1
        pydgm.control.angle_order = 2
        pydgm.control.angle_option = pydgm.angle.gl
        pydgm.control.recon_print = False
        pydgm.control.eigen_print = False
        pydgm.control.outer_print = False
        pydgm.control.recon_tolerance = 1e-14
        pydgm.control.eigen_tolerance = 1e-14
        pydgm.control.outer_tolerance = 1e-15
        pydgm.control.lamb = 1.0
        pydgm.control.use_dgm = True
        pydgm.control.store_psi = True
        pydgm.control.equation_type = 'DD'
        pydgm.control.scatter_leg_order = 0
        pydgm.control.ignore_warnings = True

    # Define methods to set various variables for the tests

    def setGroups(self, G):
        if G == 2:
            pydgm.control.xs_name = 'test/2gXS.anlxs'.ljust(256)
            pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
            pydgm.control.energy_group_map = [1, 1]
        elif G == 4:
            pydgm.control.xs_name = 'test/4gXS.anlxs'.ljust(256)
            pydgm.control.energy_group_map = [1, 1, 2, 2]
            pydgm.control.dgm_basis_name = 'test/4gbasis'.ljust(256)
        elif G == 7:
            pydgm.control.xs_name = 'test/7gXS.anlxs'.ljust(256)
            pydgm.control.dgm_basis_name = 'test/7gbasis'.ljust(256)
            pydgm.control.energy_group_map = [1, 1, 1, 1, 2, 2, 2]

    def setSolver(self, solver):
        if solver == 'fixed':
            pydgm.control.solver_type = 'fixed'.ljust(256)
            pydgm.control.source_value = 1.0
            pydgm.control.allow_fission = False
            pydgm.control.max_recon_iters = 10000
            pydgm.control.max_eigen_iters = 1
            pydgm.control.max_outer_iters = 100000
        elif solver == 'eigen':
            pydgm.control.solver_type = 'eigen'.ljust(256)
            pydgm.control.source_value = 0.0
            pydgm.control.allow_fission = True
            pydgm.control.max_recon_iters = 10000
            pydgm.control.max_eigen_iters = 10000
            pydgm.control.max_outer_iters = 1000

    def setMesh(self, mesh):
        if mesh.isdigit():
            N = int(mesh)
            pydgm.control.fine_mesh_x = [N]
            pydgm.control.coarse_mesh_x = [0.0, float(N)]
        elif mesh == 'coarse_pin':
            pydgm.control.fine_mesh_x = [3, 10, 3]
            pydgm.control.coarse_mesh_x = [0.0, 0.09, 1.17, 1.26]
        elif mesh == 'fine_pin':
            pydgm.control.fine_mesh_x = [3, 22, 3]
            pydgm.control.coarse_mesh_x = [0.0, 0.09, 1.17, 1.26]

    def setBoundary(self, bounds):
        if bounds == 'reflect':
            pydgm.control.boundary_east = 1.0
            pydgm.control.boundary_west = 1.0
        elif bounds == 'vacuum':
            pydgm.control.boundary_east = 0.0
            pydgm.control.boundary_west = 0.0

    def test_dgmsolver_solve_orders_fission(self):
        '''
        Test order 0 returns the same value when given the converged input for fixed problem
        '''

        # Set the variables for the test
        self.setSolver('fixed')
        self.setGroups(7)
        self.setMesh('1')
        self.setBoundary('vacuum')

        pydgm.control.material_map = [1]
        pydgm.control.allow_fission = False
        nA = 2

        pydgm.dgmsolver.initialize_dgmsolver()

        ########################################################################
        phi = np.array([1.0270690018072897, 1.1299037448361107, 1.031220528952085, 1.0309270835964415, 1.0404782471236467, 1.6703756546880606, 0.220435842109856])
        psi = np.array([[0.28670426208182, 0.3356992956691126, 0.3449054812807308, 0.3534008341488156, 0.3580544322663831, 0.6250475242024148, 0.0981878157679874],
                        [0.6345259657784981, 0.6872354146444389, 0.6066643580008859, 0.6019079440169605, 0.6067485919732419, 0.9472768646717264, 0.1166347906435061],
                        [0.6345259657784981, 0.6872354146444389, 0.6066643580008859, 0.6019079440169605, 0.6067485919732419, 0.9472768646717264, 0.1166347906435061],
                        [0.28670426208182, 0.3356992956691126, 0.3449054812807308, 0.3534008341488156, 0.3580544322663831, 0.6250475242024148, 0.0981878157679874]])

        phi_m_test = np.array([[2.1095601795959631, 0.0194781579525075, -0.0515640941922323, -0.0670614070008202],
                               [1.6923809227259041, 0.5798575454457766, -0.8490899895663372, 0.]])
        psi_m_test = np.array([[[0.6603549365902395, -0.0467999863865106, -0.0202498403596039, -0.0087381098484839],
                                [0.6242829410728972, 0.1837534467300195, -0.3240890486311904, 0.]],
                               [[1.2651668412203918, 0.0398970701525067, -0.0287329314249332, -0.0467550965071546],
                                [0.9645561434964076, 0.3465627924733725, -0.4781282918931471, 0.]],
                               [[1.2651668412203918, 0.0398970701525067, -0.0287329314249332, -0.0467550965071546],
                                [0.9645561434964076, 0.3465627924733725, -0.4781282918931471, 0.]],
                               [[0.6603549365902395, -0.0467999863865106, -0.0202498403596039, -0.0087381098484839],
                                [0.6242829410728972, 0.1837534467300195, -0.3240890486311904, 0.]]])

        # Set the converged fluxes
        pydgm.state.phi[0, :, 0] = phi
        for a in range(2 * nA):
            pydgm.state.psi[:, a, 0] = psi[a]
        pydgm.state.keff = 1.0
        old_psi = pydgm.state.psi

        # Get the moments from the fluxes
        pydgm.dgmsolver.compute_flux_moments()

        order = 0
        pydgm.dgm.dgm_order = order
        pydgm.state.mg_phi = pydgm.dgm.phi_m[0]
        pydgm.state.mg_psi = pydgm.dgm.psi_m[0]

        phi_m = phi_m_test[:, order]
        psi_m = psi_m_test[:, :, order]

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.compute_xs_moments()
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        np.testing.assert_array_almost_equal(pydgm.state.mg_phi.flatten(), phi_m, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(pydgm.state.mg_psi[:, a, 0].flatten(), psi_m[a], 12)

        ########################################################################
        order = 1
        pydgm.dgm.dgm_order = order
        pydgm.state.mg_phi = pydgm.dgm.phi_m[0]
        pydgm.state.mg_psi = pydgm.dgm.psi_m[0]

        phi_m = phi_m_test[:, order]
        psi_m = psi_m_test[:, :, order]

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        np.testing.assert_array_almost_equal(pydgm.state.mg_phi.flatten(), phi_m, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(pydgm.state.mg_psi[:, a, 0].flatten(), psi_m[a], 12)

        ########################################################################
        order = 2
        pydgm.dgm.dgm_order = order
        phi_m = phi_m_test[:, order]
        psi_m = psi_m_test[:, :, order]

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        np.testing.assert_array_almost_equal(pydgm.state.mg_phi.flatten(), phi_m, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(pydgm.state.mg_psi[:, a, 0].flatten(), psi_m[a], 12)

        ########################################################################
        order = 3
        pydgm.dgm.dgm_order = order
        phi_m = phi_m_test[:, order]
        psi_m = psi_m_test[:, :, order]

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        np.testing.assert_array_almost_equal(pydgm.state.mg_phi.flatten(), phi_m, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(pydgm.state.mg_psi[:, a, 0].flatten(), psi_m[a], 12)

    def test_dgmsolver_solve_orders_fixed(self):
        '''
        Test order 0 returns the same value when given the converged input for fixed problem
        '''

        # Set the variables for the test
        self.setSolver('fixed')
        self.setGroups(7)
        self.setMesh('1')
        self.setBoundary('reflect')

        pydgm.control.material_map = [1]
        pydgm.control.allow_fission = False
        nA = 2

        pydgm.dgmsolver.initialize_dgmsolver()

        ########################################################################
        order = 0
        pydgm.dgm.dgm_order = order
        # Set the converged fluxes
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        phi = np.linalg.solve((T - S), np.ones(7))
        pydgm.state.phi[0, :, 0] = phi
        for a in range(2 * nA):
            pydgm.state.psi[:, a, 0] = phi / 2.0
        pydgm.state.keff = 1.0
        old_psi = pydgm.state.psi

        # Get the moments from the fluxes
        pydgm.dgmsolver.compute_flux_moments()

        pydgm.state.mg_phi = pydgm.dgm.phi_m[0]
        pydgm.state.mg_psi = pydgm.dgm.psi_m[0]

        phi_m_test = np.array([46.0567816728045685, 39.9620014433207302])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.compute_xs_moments()
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 1
        pydgm.dgm.dgm_order = order
        pydgm.dgm.phi_m[0] = pydgm.state.mg_phi
        pydgm.dgm.psi_m[0] = pydgm.state.mg_psi

        phi_m_test = np.array([-7.7591835637013871, 18.2829496616545661])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 2
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-10.382535949686881, -23.8247979105656675])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 3
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-7.4878268473063185, 0.0])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

    def test_dgmsolver_solve_orders(self):
        '''
        Test order 0 returns the same value when given the converged input for eigen problem
        '''

        # Set the variables for the test
        self.setSolver('eigen')
        self.setGroups(7)
        self.setMesh('1')
        self.setBoundary('reflect')
        pydgm.control.material_map = [1]
        nA = 2

        pydgm.dgmsolver.initialize_dgmsolver()

        ########################################################################
        order = 0
        pydgm.dgm.dgm_order = order
        # Set the converged fluxes
        phi = np.array([0.198933535568562, 2.7231683533646702, 1.3986600409998782, 1.010361903429942, 0.8149441787223116, 0.8510697418684054, 0.00286224604623])
        pydgm.state.phi[0, :, 0] = phi
        for a in range(2 * nA):
            with self.subTest(a=a):
                pydgm.state.psi[:, a, 0] = phi / 2.0
        pydgm.state.keff = 1.0674868709852505
        old_psi = pydgm.state.psi

        # Get the moments from the fluxes
        pydgm.dgmsolver.compute_flux_moments()

        pydgm.state.mg_phi = pydgm.dgm.phi_m[0]
        pydgm.state.mg_psi = pydgm.dgm.psi_m[0]

        phi_m_test = np.array([2.6655619166815265, 0.9635261040519922])
        norm_frac = 2 / sum(phi_m_test)
        phi_m_test *= norm_frac

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.compute_xs_moments()
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        assert_almost_equal(pydgm.state.keff, 1.0674868709852505, 12)

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 1
        pydgm.dgm.dgm_order = order
        pydgm.dgm.phi_m[0] = pydgm.state.mg_phi
        pydgm.dgm.psi_m[0] = pydgm.state.mg_psi

        phi_m_test = np.array([-0.2481536345018054, 0.5742286414743346])
        phi_m_test *= norm_frac

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 2
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-1.4562664776830221, -0.3610274595244746])
        phi_m_test *= norm_frac

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

        ########################################################################
        order = 3
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-1.0699480859043353, 0.0])
        phi_m_test *= norm_frac

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, nA:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten(), phi_m_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(psi_m[:, a, 0].flatten(), 0.5 * phi_m_test, 12)

    def test_dgmsolver_solve_orders_eigen(self):
        '''
        Test order 0 returns the same value when given the converged input for eigen problem
        '''
        # Set the variables for the test
        self.setSolver('eigen')
        self.setGroups(7)
        pydgm.control.fine_mesh_x = [2, 1, 2]
        pydgm.control.coarse_mesh_x = [0.0, 5.0, 6.0, 11.0]
        pydgm.control.material_map = [1, 5, 3]
        self.setBoundary('vacuum')
        pydgm.control.angle_order = 4
        pydgm.control.xs_name = 'test/alt_7gXS.anlxs'.ljust(256)

        pydgm.control.recon_print = 0
        pydgm.control.eigen_print = 0
        pydgm.control.outer_print = 0
        pydgm.control.inner_print = 0

        pydgm.control.max_recon_iters = 1
        pydgm.control.max_eigen_iters = 1
        pydgm.control.max_outer_iters = 1
        pydgm.control.max_inner_iters = 1

        pydgm.dgmsolver.initialize_dgmsolver()

        ########################################################################
        order = 0
        pydgm.dgm.dgm_order = order
        # Set the converged fluxes
        phi = np.array([[[1.6242342173603628, 1.6758532156636183, 0.8405795956015387, 0.1625775747329378, 0.1563516098298166, 0.1085336308306435, 0.0620903836758187],
                         [2.6801570555785044, 3.0677447677828793, 1.449823985768667, 0.2681250437495656, 0.223283519933589, 0.1450135178081014, 0.0801799450539108],
                         [3.2427808456629887, 3.6253236761323215, 1.5191384960457082, 0.2657137576543584, 0.1710313947880435, 0.0951334377954927, 0.0425020905708747],
                         [3.078740985037656, 3.2970204075028375, 1.4972548403087522, 0.2419744554249777, 0.1399415224162651, 0.0804404829573202, 0.0429420231808826],
                         [2.025799210421367, 1.9237182726014126, 0.8984917270995029, 0.1359184813858208, 0.0691590845219909, 0.0395429438436025, 0.0228838012778573]]])
        psi = np.array([[[0.222079350493803, 0.367893748426737, 0.2235158737950531, 0.0432849735160482, 0.0463727895022187, 0.0355187175888715, 0.0228020647902731],
                         [0.2550513848467887, 0.4086506508949974, 0.2437587461588053, 0.0472221628586482, 0.0500292057938681, 0.0378826318416084, 0.0239178952309458],
                         [0.3382749040753765, 0.5005376956437221, 0.286799618688869, 0.0556029704482913, 0.0575482625391845, 0.0425783497502043, 0.0260285263773904],
                         [0.5750074909228001, 0.6987878823386922, 0.3690096305377114, 0.0716465574529971, 0.0710147551998868, 0.050472013809047, 0.029289670734657],
                         [1.0537788563447283, 0.9734181137831549, 0.4957923512162933, 0.0961929513181893, 0.0917160223956373, 0.0619693328895713, 0.0340926844459002],
                         [1.3255267239562842, 1.1718393856235512, 0.5467264435687115, 0.106076277173514, 0.0986556746148473, 0.0659669292501365, 0.0361998578074773],
                         [1.344743505152009, 1.275694892110874, 0.5780321815222638, 0.1109128207385084, 0.1003555995219249, 0.0669432975064532, 0.0368743872958025],
                         [1.3169150639303029, 1.3131431962945315, 0.5934134444747582, 0.112983521080786, 0.1006890422223745, 0.0671233256092146, 0.0370834493694713]],
                        [[0.6885553482025526, 1.089335039975068, 0.6069001661447114, 0.1149124812343551, 0.1081129453446089, 0.0743840699002204, 0.0426285473144128],
                         [0.7725107502337766, 1.172471051868116, 0.6392311814456784, 0.1209778691436543, 0.112132068182718, 0.0761388322283501, 0.0430146562230251],
                         [0.9634060077282145, 1.3324269934504407, 0.6954805007449582, 0.1314528956036147, 0.118327409011439, 0.0784415022220629, 0.0433112324654103],
                         [1.3418218650264861, 1.5478745404418306, 0.7556888528998005, 0.1422593096610216, 0.1224628337686979, 0.0787659469902519, 0.0426536374845071],
                         [1.729477941003646, 1.6974160643540823, 0.7442585512313288, 0.1383544390474219, 0.1120623770468576, 0.0714367487802417, 0.0391794498708677],
                         [1.7051696722305358, 1.751812196905169, 0.7582694132424415, 0.1369370337610382, 0.1046797020301904, 0.0665917118269666, 0.0368374928147647],
                         [1.5387508951279656, 1.7186389175341759, 0.7620051265765969, 0.135317553737312, 0.1007482443032926, 0.0640130246749766, 0.03564770613761],
                         [1.4364950427473613, 1.6792136928011256, 0.7579125860583991, 0.1336344485909219, 0.098604182325654, 0.0626567122928802, 0.0350590921713212]],
                        [[1.0637855120993567, 1.536007235058809, 0.7512967906309741, 0.1404630994676566, 0.1148056366649365, 0.0698763787160453, 0.0333956120236536],
                         [1.1772365412120178, 1.623439996483817, 0.7691016739211279, 0.1437011859524629, 0.1139120708369216, 0.0675556535748025, 0.0312946245257323],
                         [1.4167593249106138, 1.7678192897287501, 0.7810108616578451, 0.1455407088176891, 0.107675105342892, 0.0605018605823794, 0.026386507283148],
                         [1.7904939585505957, 1.89352053932841, 0.7181697463659802, 0.1317868631490471, 0.082793577541892, 0.0420585740741061, 0.0164782671802563],
                         [2.1207386621923865, 1.9637650446071278, 0.7212071824348782, 0.12113922754426, 0.0658334448866402, 0.034958078599678, 0.0145491386909295],
                         [1.7517468797848386, 1.8958105952103985, 0.798043960365745, 0.1300892526694405, 0.0723937875679986, 0.0403303303934091, 0.0189198483739351],
                         [1.467070365430227, 1.7596888439540126, 0.7918720366437686, 0.1285518126305569, 0.0733074589055889, 0.041586719950917, 0.0205120079897094],
                         [1.3289690484789758, 1.6715864407056662, 0.7760283202736972, 0.1259707834617701, 0.07292702807355, 0.041730732082634, 0.0210874065276817]],
                        [[1.3742390593834137, 1.6804507107489854, 0.7616179736173394, 0.1299769203242264, 0.0826519306543626, 0.0473735675866383, 0.0231585138707784],
                         [1.49144934721379, 1.7347522148427128, 0.7689492552815056, 0.1302419543122088, 0.0802672835477712, 0.0454900456157048, 0.0223847678848062],
                         [1.7148976537965404, 1.8047767702734685, 0.7718681965783076, 0.1284953242691218, 0.0749924134827408, 0.042038811478865, 0.0212660172635992],
                         [1.9823521863053744, 1.824301962488276, 0.7671582509538742, 0.1232633853173764, 0.0683865153826584, 0.0389703997168544, 0.0208888756568808],
                         [1.766407427859224, 1.725997639499484, 0.7874221794566647, 0.1232544708010276, 0.0685805464349633, 0.0397831546607478, 0.0217985791844457],
                         [1.2599720527733733, 1.49648379942603, 0.7295310940574015, 0.1149891560923702, 0.0655143483522853, 0.0382708203491909, 0.0214214755581922],
                         [1.0082273816890912, 1.3201786458724547, 0.6726845915892845, 0.1067770556462346, 0.0623342020910217, 0.0366918535944347, 0.0209491303191844],
                         [0.8979420792671616, 1.2278028414312567, 0.6395952779081429, 0.1019260121956693, 0.0603514150340045, 0.0356908055351527, 0.0206234908394634]],
                        [[1.4648855138220889, 1.4418670068930663, 0.623563195498159, 0.0946670238578062, 0.0444506293512766, 0.0243640916897312, 0.0133250773869966],
                         [1.5309495376107136, 1.4197218176391437, 0.6102323454639805, 0.0916160580458327, 0.0427338663841867, 0.0237604956146663, 0.0133235079710548],
                         [1.6038006670473024, 1.339896091825747, 0.5814786019156777, 0.0859079287167494, 0.0407949773027919, 0.0233252278905371, 0.0133720031593783],
                         [1.4598645444698681, 1.1444682238971755, 0.5306971842723684, 0.0785437229491508, 0.039713913866885, 0.0228212778870397, 0.0128190133645811],
                         [0.7372082396801695, 0.8130863049868733, 0.3980411128911099, 0.0611423034295212, 0.0323171553205731, 0.0184328283005457, 0.0106824936928838],
                         [0.4329105987588648, 0.5823444079707099, 0.3100178712779538, 0.0484740605658099, 0.0272440970357683, 0.0158582531655901, 0.0096058269236477],
                         [0.3261965462563942, 0.4754151246434862, 0.2637847730312079, 0.0416367506767501, 0.0242295879053059, 0.0142777111873078, 0.0088952657992601],
                         [0.2839554762443687, 0.4279896897990576, 0.2420050678428891, 0.0383706034304901, 0.0227129595199266, 0.0134676747135594, 0.0085151463676417]]])
        # psi /= (np.linalg.norm(psi) * 10)
        phi_new = phi * 0
        for a in range(pydgm.control.number_angles):
            phi_new[0] += psi[:, a, :] * pydgm.angle.wt[a]
            phi_new[0] += psi[:, 2 * pydgm.control.number_angles - a - 1, :] * pydgm.angle.wt[a]

        for c in range(5):
            for g in range(7):
                pydgm.state.phi[0, :, c] = phi[0, c]
                for a in range(8):
                    pydgm.state.psi[g, a, c] = psi[c, a, g]
        pydgm.state.keff = 0.33973731848126831
        old_psi = pydgm.state.psi

        # Get the moments from the fluxes
        pydgm.dgmsolver.compute_flux_moments()

        pydgm.state.mg_phi = pydgm.dgm.phi_m[0]
        pydgm.state.mg_psi = pydgm.dgm.psi_m[0]

        phi_m_test = pydgm.dgm.phi_m[0].flatten('F')
        phi_m_test /= np.linalg.norm(phi_m_test, 1) / 10

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, pydgm.control.number_angles:, 0]
        pydgm.dgmsolver.compute_xs_moments()
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.flatten('F'), phi_m_test, 12)

        ########################################################################
        order = 1
        pydgm.dgm.dgm_order = order
        pydgm.dgm.phi_m[0] = pydgm.state.mg_phi
        pydgm.dgm.psi_m[0] = pydgm.state.mg_psi

        phi_m_test = np.array([0.66268605409797898, 1.1239769588944581, 1.4011457517310117, 1.3088156391543195, 0.84988298005049157, 3.7839914869954847E-002, 5.7447025802385317E-002, 5.1596378790218486E-002, 3.8939158159247110E-002, 1.8576596655769165E-002])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, pydgm.control.number_angles:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.T.flatten('F'), phi_m_test, 12)

        ########################################################################
        order = 2
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-0.20710920655711104, -0.44545552454860282, -0.46438347612912256, -0.41828263508757896, -0.18748642683048020, 3.1862102568187112E-004, 3.1141556263365915E-003, 5.3924924332473369E-003, 5.0995287080187754E-003, 3.0030380436572414E-003])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, pydgm.control.number_angles:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.T.flatten('F'), phi_m_test, 12)

        ########################################################################
        order = 3
        pydgm.dgm.dgm_order = order
        phi_m_test = np.array([-0.13255187402833862, -0.30996650357216082, -0.42418668341792881, -0.32530149073950271, -0.15053175043041164, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000])

        pydgm.state.mg_incident_x = pydgm.dgm.psi_m[order, :, pydgm.control.number_angles:, 0]
        pydgm.dgmsolver.slice_xs_moments(order)

        pydgm.solver.solve()

        phi_m = pydgm.state.mg_phi
        psi_m = pydgm.state.mg_psi

        np.testing.assert_array_almost_equal(phi_m.T.flatten('F'), phi_m_test, 12)

    def test_dgmsolver_unfold_flux_moments(self):
        '''
        Test unfolding flux moments into the scalar and angular fluxes
        '''
        self.setGroups(7)
        self.setSolver('fixed')
        self.setMesh('1')
        pydgm.control.material_map = [1]
        self.setBoundary('reflect')

        pydgm.state.initialize_state()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        phi_test = np.linalg.solve((T - S), np.ones(7))
        # Compute the moments directly
        basis = np.loadtxt('test/7gbasis').T
        phi_m = basis.dot(phi_test)
        phi_m.resize(2, 4)
        for i in range(4):
            pydgm.dgm.phi_m[i, 0, :, 0] = phi_m[:, i]

        # Assume infinite homogeneous media (isotropic flux)
        for a in range(4):
            pydgm.dgm.psi_m[:, :, a, :] = 0.5 * pydgm.dgm.phi_m[:, 0, :, :]

        pydgm.dgmsolver.unfold_flux_moments()

        np.testing.assert_array_almost_equal(pydgm.state.phi.flatten(), phi_test, 12)
        for a in range(4):
            with self.subTest(a=a):
                np.testing.assert_array_almost_equal(pydgm.state.psi[:, a, 0].flatten(), phi_test * 0.5)

    def test_dgmsolver_vacuum1(self):
        '''
        Test the 7g->2G dgm fixed source problem with vacuum boundary conditions

        Using pin cell geometry with 3 material regions

        with fission
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('fixed')
        self.setMesh('fine_pin')
        self.setBoundary('vacuum')
        pydgm.control.material_map = [5, 1, 5]
        pydgm.control.angle_order = 10
        pydgm.control.allow_fission = True
        pydgm.control.lamb = 0.55
        pydgm.control.source_value = 1.0

        pydgm.dgmsolver.initialize_dgmsolver()

        phi_test = [1.6274528794638465, 2.71530879612549, 1.461745652768521, 1.3458703902580473, 1.3383852126342237, 1.9786760428590306, 0.24916735316863525, 1.6799175379390339, 2.8045999684695797, 1.516872017690622, 1.3885229934177148, 1.3782095743929001, 2.051131534663419, 0.26873064494111804, 1.728788120766425, 2.883502682394886, 1.5639999234445578, 1.4246328795261316, 1.4121166958899956, 2.1173467066121874, 0.2724292532553828, 1.7839749586964595, 2.990483236041222, 1.6474286521554664, 1.5039752034511047, 1.4924425499449177, 2.3127049909257686, 0.25496633574011124, 1.8436202405517381, 3.122355600505027, 1.7601872542791979, 1.61813693117119, 1.6099652659907275, 2.60256939853679, 0.24873883482629144, 1.896225857094417, 3.2380762891116794, 1.8534459525081792, 1.7117690484677541, 1.7061424886519436, 2.831599567019092, 0.26081315241625463, 1.9421441425092316, 3.338662519105913, 1.9310368092514267, 1.789369188781964, 1.7857603538028388, 3.0201767784594478, 0.2667363594339594, 1.9816803882995633, 3.424961908919033, 1.9955392685572624, 1.853808027881203, 1.851843446016314, 3.1773523146671065, 0.27189861962890616, 2.0150973757748596, 3.4976972455932094, 2.0486999251118014, 1.9069365316531377, 1.9063232414331912, 3.307833351001605, 0.2755922553419729, 2.042616213943685, 3.5574620224059217, 2.0917047787489365, 1.9499600832109016, 1.9504462746103806, 3.4141788518658602, 0.27833708525534473, 2.0644181962111365, 3.604732065595381, 2.1253588124042495, 1.9836690960190415, 1.985023407898914, 3.497921277464179, 0.28030660972118154, 2.080646338594525, 3.6398748475310785, 2.150203190885212, 2.0085809732608575, 2.0105818574623395, 3.5600286331289643, 0.2816665790912415, 2.0914067095511766, 3.663158139593214, 2.16659102830272, 2.0250269209204395, 2.0274573320958647, 3.6011228563902344, 0.2825198396790823, 2.0967694470675315, 3.6747566727970047, 2.174734975618102, 2.033203922754008, 2.0358487486465924, 3.621580567528384, 0.28293121918903963, 2.0967694470675315, 3.6747566727970042, 2.1747349756181023, 2.033203922754008, 2.0358487486465924, 3.6215805675283836, 0.2829312191890396, 2.0914067095511766, 3.6631581395932136, 2.1665910283027205, 2.02502692092044, 2.0274573320958647, 3.6011228563902358, 0.2825198396790823, 2.080646338594525, 3.639874847531079, 2.150203190885212, 2.008580973260857, 2.01058185746234, 3.5600286331289652, 0.2816665790912415, 2.0644181962111365, 3.6047320655953805, 2.125358812404249, 1.9836690960190408, 1.985023407898914, 3.4979212774641804, 0.2803066097211815, 2.042616213943685, 3.5574620224059217, 2.0917047787489365, 1.9499600832109014, 1.9504462746103808, 3.4141788518658616, 0.2783370852553448, 2.01509737577486, 3.49769724559321, 2.0486999251118005, 1.9069365316531375, 1.9063232414331914, 3.3078333510016056, 0.27559225534197296, 1.981680388299563, 3.424961908919033, 1.9955392685572624, 1.8538080278812032, 1.8518434460163142, 3.1773523146671074, 0.27189861962890616, 1.9421441425092318, 3.338662519105913, 1.931036809251427, 1.7893691887819645, 1.7857603538028393, 3.020176778459449, 0.2667363594339594, 1.896225857094417, 3.2380762891116777, 1.8534459525081792, 1.7117690484677544, 1.706142488651944, 2.831599567019092, 0.2608131524162547, 1.8436202405517386, 3.122355600505027, 1.7601872542791974, 1.6181369311711902, 1.6099652659907278, 2.6025693985367897, 0.24873883482629144, 1.783974958696459, 2.990483236041223, 1.6474286521554669, 1.5039752034511054, 1.4924425499449177, 2.312704990925769, 0.2549663357401113, 1.7287881207664255, 2.883502682394885, 1.5639999234445578, 1.4246328795261323, 1.412116695889996, 2.117346706612188, 0.27242925325538286, 1.6799175379390343, 2.8045999684695793, 1.516872017690622, 1.388522993417715, 1.3782095743929004, 2.05113153466342, 0.26873064494111826, 1.6274528794638465, 2.7153087961254894, 1.4617456527685213, 1.3458703902580476, 1.3383852126342235, 1.978676042859031, 0.24916735316863528]
        pydgm.state.phi[0, :, :] = np.reshape(phi_test, (7, 28), 'F')

        pydgm.dgmsolver.dgmsolve()

        np.testing.assert_array_almost_equal(pydgm.state.phi[0].flatten('F'), phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]

        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_reflect1(self):
        '''
        Test the 7g->2G, fixed source, infinite medium problem

        Uses 3 spatial regions with the same material in each

        no fission
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('fixed')
        self.setMesh('fine_pin')
        self.setBoundary('reflect')
        pydgm.control.material_map = [1, 1, 1]
        pydgm.control.angle_order = 10
        pydgm.control.lamb = 0.45

        pydgm.dgmsolver.initialize_dgmsolver()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        phi_test = np.linalg.solve((T - S), np.ones(7))
        phi_test = np.array([phi_test for i in range(28)]).flatten()

        pydgm.dgmsolver.dgmsolve()

        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :].flatten('F'), phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_vacuum2(self):
        '''
        Test the 7g->2G, fixed source problem with vacuum conditions

        Uses one spatial cell, no fission
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('fixed')
        self.setMesh('1')
        self.setBoundary('vacuum')
        pydgm.control.material_map = [1]
        pydgm.control.lamb = 0.76
        pydgm.control.allow_fission = True
        phi_test = np.array([1.0781901438738859, 1.5439788126739036, 1.0686290157458673, 1.0348940034466163, 1.0409956199943164, 1.670442207080332, 0.2204360523334687])

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Set the test flux
        pydgm.state.phi[0, :, 0] = phi_test
        for a in range(4):
            pydgm.state.psi[:, a, 0] = 0.5 * phi_test

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the scalar flux
        np.testing.assert_array_almost_equal(pydgm.state.phi[0].flatten('F'), phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_reflect2(self):
        '''
        Test the 7g->2G, fixed source problem with infinite medium and one spatial cell
        '''

        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('fixed')
        self.setMesh('1')
        self.setBoundary('reflect')
        pydgm.control.material_map = [1]
        pydgm.control.equation_type = 'DD'
        pydgm.control.lamb = 0.4

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        phi_test = np.linalg.solve((T - S), np.ones(7))

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the scalar flux
        np.testing.assert_array_almost_equal(pydgm.state.phi[0].flatten('F'), phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenV2g(self):
        '''
        Test the 2g->1G, eigenvalue problem with 1 medium and vacuum conditions
        '''

        # Set the variables for the test
        self.setGroups(2)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('vacuum')
        pydgm.control.material_map = [1]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Set the test flux
        phi_test = np.array([0.7263080826036219, 0.12171194697729938, 1.357489062141697, 0.2388759408761157, 1.8494817499319578, 0.32318764022244134, 2.199278050699694, 0.38550684315075284, 2.3812063412628075, 0.4169543421336097, 2.381206341262808, 0.41695434213360977, 2.1992780506996943, 0.38550684315075295, 1.8494817499319585, 0.3231876402224415, 1.3574890621416973, 0.23887594087611572, 0.7263080826036221, 0.12171194697729937])

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, 0.8099523232983424, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenV4g(self):
        '''
        Test the 4g->2G, eigenvalue problem with 1 medium and vacuum conditions
        '''
        # Set the variables for the test
        self.setGroups(4)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('vacuum')
        pydgm.control.material_map = [1]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Set the test flux
        phi_test = np.array([1.6283945282803138, 1.2139688020213637, 0.03501217302426163, 6.910819115000905e-17, 1.9641731545343404, 1.59852298044156, 0.05024813427412045, 1.0389359842780806e-16, 2.2277908375593736, 1.8910978193073922, 0.061518351747482505, 1.3055885402420332e-16, 2.40920191588961, 2.088554929299159, 0.06902375359471126, 1.487795240822353e-16, 2.5016194254000244, 2.188087672560707, 0.0727855220655801, 1.5805185521208351e-16, 2.501619425400025, 2.1880876725607075, 0.07278552206558009, 1.5805185521208351e-16, 2.40920191588961, 2.088554929299159, 0.06902375359471127, 1.487795240822353e-16, 2.2277908375593736, 1.891097819307392, 0.0615183517474825, 1.3055885402420332e-16, 1.9641731545343404, 1.59852298044156, 0.05024813427412045, 1.0389359842780806e-16, 1.6283945282803138, 1.2139688020213637, 0.03501217302426163, 6.910819115000904e-17])

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, 0.185134666261, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenV7g(self):
        '''
        Test the 7g->2G, eigenvalue problem with 1 medium and vacuum conditions
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('vacuum')
        pydgm.control.material_map = [1]
        pydgm.control.lamb = 0.4

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Set the test flux
        phi_test = np.array([0.19050251326520584, 1.9799335510805185, 0.69201814518126, 0.3927000245492841, 0.2622715078950253, 0.20936059119838546, 0.000683954269595958, 0.25253653423327665, 2.8930819653774895, 1.158606945184528, 0.6858113244922716, 0.4639601075261923, 0.4060114930207368, 0.0013808859451732852, 0.30559047625122115, 3.6329637815416556, 1.498034484581793, 0.9026484213739354, 0.6162114941108023, 0.5517562407150877, 0.0018540270157502057, 0.3439534785160265, 4.153277746375052, 1.7302149163096785, 1.0513217539517374, 0.7215915434720093, 0.653666204542615, 0.0022067618449436725, 0.36402899896324237, 4.421934793951583, 1.8489909842118943, 1.127291245982061, 0.7756443978822711, 0.705581398687358, 0.0023773065003326204, 0.36402899896324237, 4.421934793951582, 1.8489909842118946, 1.1272912459820612, 0.7756443978822711, 0.705581398687358, 0.0023773065003326204, 0.34395347851602653, 4.153277746375052, 1.7302149163096785, 1.0513217539517377, 0.7215915434720092, 0.653666204542615, 0.002206761844943672, 0.3055904762512212, 3.6329637815416564, 1.498034484581793, 0.9026484213739353, 0.6162114941108023, 0.5517562407150877, 0.0018540270157502063, 0.2525365342332767, 2.8930819653774895, 1.1586069451845278, 0.6858113244922716, 0.4639601075261923, 0.4060114930207368, 0.0013808859451732852, 0.19050251326520584, 1.9799335510805192, 0.6920181451812601, 0.3927000245492842, 0.26227150789502535, 0.20936059119838543, 0.0006839542695959579])

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, 0.30413628310914226, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    # Test the eigenvalue solver for infinite media

    def test_dgmsolver_eigenR2g(self):
        '''
        Test the 2g->1G, eigenvalue problem with infinite medium
        '''
        # Set the variables for the test
        self.setGroups(2)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('reflect')
        pydgm.control.lamb = 0.7
        pydgm.control.material_map = [1]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        X = np.outer(pydgm.material.chi[:, 0], pydgm.material.nu_sig_f[:, 0])

        keff, phi = np.linalg.eig(np.linalg.inv(T - S).dot(X))

        i = np.argmax(keff)
        keff_test = keff[i]
        phi_test = phi[:, i]

        phi_test = np.array([phi_test for i in range(10)]).flatten()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, keff_test, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenR4g(self):
        '''
        Test the 4g->2G, eigenvalue problem with infinite medium
        '''
        # Set the variables for the test
        self.setGroups(4)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('reflect')
        pydgm.control.material_map = [1]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        X = np.outer(pydgm.material.chi[:, 0], pydgm.material.nu_sig_f[:, 0])

        keff, phi = np.linalg.eig(np.linalg.inv(T - S).dot(X))
        i = np.argmax(keff)
        keff_test = keff[i]
        phi_test = phi[:, i]

        phi_test = np.array([phi_test for i in range(10)]).flatten()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, keff_test, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenR7g(self):
        '''
        Test the 7g->2G, eigenvalue problem with infinite medium
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('eigen')
        self.setMesh('10')
        self.setBoundary('reflect')
        pydgm.control.material_map = [1]
        pydgm.control.lamb = 0.46

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Compute the test flux
        T = np.diag(pydgm.material.sig_t[:, 0])
        S = pydgm.material.sig_s[0, :, :, 0].T
        X = np.outer(pydgm.material.chi[:, 0], pydgm.material.nu_sig_f[:, 0])

        keff, phi = np.linalg.eig(np.linalg.inv(T - S).dot(X))
        keff = np.real(keff)
        i = np.argmax(keff)
        keff_test = keff[i]
        phi_test = phi[:, i]

        phi_test = np.array([phi_test for i in range(10)]).flatten()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        assert_almost_equal(pydgm.state.keff, keff_test, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    # Test the eigenvalue solver for pin cell like problems

    def test_dgmsolver_eigenR2gPin(self):
        '''
        Test the 2g->1G, eigenvalue problem on a pin cell of
            water | fuel | water
        with reflective conditions
        '''
        # Set the variables for the test
        self.setGroups(2)
        self.setSolver('eigen')
        self.setMesh('coarse_pin')
        self.setBoundary('reflect')
        pydgm.control.material_map = [2, 1, 2]
        pydgm.control.lamb = 0.7

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # set the test flux
        keff_test = 0.8418546852484950
        phi_test = [0.13393183108467394, 0.04663240631432256, 0.13407552941360298, 0.04550808086281801, 0.13436333428621713, 0.043206841474147446, 0.1351651393398092, 0.0384434752119791, 0.13615737742196526, 0.03329929560434661, 0.13674284660888314, 0.030464508103354708, 0.13706978363298242, 0.028970199506203023, 0.13721638515632006, 0.028325674662651124, 0.13721638515632006, 0.028325674662651124, 0.1370697836329824, 0.028970199506203012, 0.13674284660888308, 0.0304645081033547, 0.13615737742196524, 0.03329929560434659, 0.13516513933980914, 0.03844347521197908, 0.13436333428621713, 0.043206841474147425, 0.13407552941360296, 0.045508080862818004, 0.1339318310846739, 0.046632406314322555]

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenR4gPin(self):
        '''
        Test the 4g->2G, eigenvalue problem on a pin cell of
            water | fuel | water
        with reflective conditions
        '''
        # Set the variables for the test
        self.setGroups(4)
        self.setSolver('eigen')
        self.setMesh('coarse_pin')
        self.setBoundary('reflect')
        pydgm.control.material_map = [2, 1, 2]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # set the test flux
        keff_test = 0.759180925837
        phi_test = [2.22727714687889, 1.7369075872008062, 0.03381777446256108, 1.7036045485771946e-51, 2.227312836950116, 1.737071399085861, 0.033828681689533874, 1.698195884848375e-51, 2.2273842137861877, 1.737399076914814, 0.03385050700298498, 1.6965081411970257e-51, 2.2275366771427696, 1.738049905609514, 0.033892498696060584, 1.697491400636173e-51, 2.2277285082016354, 1.7388423494826295, 0.03394281751690741, 1.6984869893367e-51, 2.2278725176984917, 1.7394359801217965, 0.03398044173136341, 1.697888141875072e-51, 2.2279685888050587, 1.739831399863755, 0.03400546998960266, 1.6957049057554318e-51, 2.2280166437743327, 1.7400290096083806, 0.034017967785934036, 1.691942073409801e-51, 2.2280166437743327, 1.7400290096083808, 0.03401796778593402, 1.68659920584123e-51, 2.2279685888050587, 1.7398313998637547, 0.03400546998960263, 1.6796706200591657e-51, 2.2278725176984917, 1.7394359801217967, 0.03398044173136335, 1.6711453402288656e-51, 2.227728508201635, 1.73884234948263, 0.033942817516907337, 1.6610070122205585e-51, 2.2275366771427696, 1.7380499056095144, 0.0338924986960605, 1.6492337810058256e-51, 2.227384213786188, 1.7373990769148142, 0.03385050700298487, 1.6385765949262272e-51, 2.2273128369501163, 1.7370713990858613, 0.03382868168953376, 1.631610014066153e-51, 2.2272771468788894, 1.7369075872008064, 0.03381777446256096, 1.6281341640813905e-51]

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 11)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_eigenR7gPin(self):
        '''
        Test the 7g->2G, eigenvalue problem on a pin cell of
            water | fuel | water
        with reflective conditions
        '''
        # Set the variables for the test
        self.setGroups(7)
        self.setSolver('eigen')
        self.setMesh('coarse_pin')
        self.setBoundary('reflect')
        pydgm.control.material_map = [5, 1, 5]
        pydgm.control.lamb = 0.43

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # set the test flux
        keff_test = 1.0794314789325041
        phi_test = [0.18617101855192203, 2.858915338372074, 1.4772041911943246, 1.0299947729491368, 0.7782291112252604, 0.6601323950057741, 0.0018780861364841711, 0.18615912584783736, 2.8586649211715436, 1.4771766639520822, 1.030040359498237, 0.7782969794725844, 0.6603312122972236, 0.0018857945539742516, 0.18613533094381535, 2.858163988201594, 1.4771216026067822, 1.0301315410919691, 0.7784327301908717, 0.6607289506819793, 0.001901260571677254, 0.1860688679764812, 2.856246121648244, 1.4768054633757053, 1.0308126366153867, 0.7795349485104974, 0.6645605858759833, 0.0020390343478796447, 0.18597801819761287, 2.8534095558345967, 1.4763058823653368, 1.0319062100766097, 0.7813236329806805, 0.6707834262470258, 0.002202198406120643, 0.18591115233580913, 2.851306298580461, 1.4759330573010532, 1.0327026586727457, 0.7826354049117061, 0.6752310599415209, 0.002251216654318464, 0.18586715682184884, 2.8499152893733255, 1.4756853599772022, 1.0332225362074143, 0.7834960048959739, 0.6780933062272468, 0.0022716374303459433, 0.1858453299832966, 2.8492230801887986, 1.475561761882258, 1.0334791905008067, 0.7839221795374745, 0.6794942839316992, 0.002280077669362046, 0.18584532998329656, 2.8492230801887986, 1.475561761882258, 1.0334791905008065, 0.7839221795374745, 0.6794942839316991, 0.0022800776693620455, 0.18586715682184884, 2.8499152893733255, 1.4756853599772024, 1.0332225362074146, 0.7834960048959738, 0.6780933062272467, 0.002271637430345943, 0.18591115233580915, 2.851306298580461, 1.4759330573010532, 1.0327026586727457, 0.7826354049117062, 0.6752310599415207, 0.0022512166543184635, 0.1859780181976129, 2.853409555834596, 1.476305882365337, 1.0319062100766097, 0.7813236329806805, 0.6707834262470258, 0.002202198406120643, 0.1860688679764812, 2.856246121648244, 1.4768054633757055, 1.0308126366153867, 0.7795349485104973, 0.6645605858759831, 0.002039034347879644, 0.18613533094381537, 2.858163988201594, 1.4771216026067824, 1.0301315410919691, 0.7784327301908716, 0.6607289506819792, 0.0019012605716772534, 0.1861591258478374, 2.858664921171543, 1.4771766639520822, 1.0300403594982372, 0.7782969794725842, 0.6603312122972235, 0.0018857945539742511, 0.18617101855192209, 2.8589153383720736, 1.477204191194325, 1.0299947729491368, 0.7782291112252603, 0.660132395005774, 0.0018780861364841707]

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 12)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 11)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_homogenize_xs_moments(self):
        '''
        Make sure that the cross sections are being properly homogenized
        '''
        self.setGroups(2)
        pydgm.control.dgm_basis_name = 'test/2gdelta'.ljust(256)
        pydgm.control.energy_group_map = [1, 2]
        self.setSolver('fixed')
        pydgm.control.allow_fission = True
        self.setBoundary('reflect')
        pydgm.control.fine_mesh_x = [2, 3, 3, 2]
        pydgm.control.coarse_mesh_x = [0.0, 1.0, 2.0, 4.0, 4.5]
        pydgm.control.material_map = [1, 2, 1, 2]
        pydgm.control.homogenization_map = [1, 1, 2, 3, 3, 3, 4, 4, 4, 5]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()
        pydgm.dgmsolver.compute_flux_moments()
        pydgm.dgmsolver.compute_xs_moments()

        # Check sig_t
        sig_t_test = np.array([[1.0, 2.0],
                               [1.0, 3.0],
                               [1.0, 2.5],
                               [1.0, 2.1578947368421],
                               [1.0, 3.0]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_sig_t, sig_t_test.T, 12)

        # Check nu_sig_f
        nu_sig_f_test = np.array([[0.5, 0.5],
                                  [0.0, 0.0],
                                  [0.25, 0.25],
                                  [0.4210526315789470, 0.4210526315789470],
                                  [0.0, 0.0]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_nu_sig_f, nu_sig_f_test.T, 12)

        # Check sig_s
        sig_s_test = np.array([[[0.3, 0.8, 0.55, 0.378947368421053, 0.8],
                                [0.3, 1.2, 0.75, 0.442105263157895, 1.2]],
                               [[0., 0., 0., 0., 0.],
                                [0.3, 1.2, 0.75, 0.442105263157895, 1.2]]])

        np.testing.assert_array_almost_equal(pydgm.dgm.sig_s_m[0, :, :, :, 0], sig_s_test, 12)

    def test_dgmsolver_homogenize_xs_moments_2(self):
        '''
        Make sure that the cross sections are being properly homogenized
        '''
        self.setGroups(2)
        pydgm.control.dgm_basis_name = 'test/2gdelta'.ljust(256)
        pydgm.control.energy_group_map = [1, 2]
        self.setSolver('fixed')
        pydgm.control.allow_fission = True
        self.setBoundary('reflect')
        pydgm.control.fine_mesh_x = [2, 3, 3, 2]
        pydgm.control.coarse_mesh_x = [0.0, 1.0, 2.0, 4.0, 4.5]
        pydgm.control.material_map = [1, 2, 1, 2]
        pydgm.control.homogenization_map = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()
        pydgm.dgmsolver.compute_flux_moments()
        pydgm.dgmsolver.compute_xs_moments()

        # Check sig_t
        sig_t_test = np.array([[1.0, 2.44],
                               [1.0, 2.24137931034483]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_sig_t, sig_t_test.T, 12)

        # Check nu_sig_f
        nu_sig_f_test = np.array([[0.28, 0.28],
                                  [0.3793103448275860, 0.3793103448275860]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_nu_sig_f, nu_sig_f_test.T, 12)

        # Check sig_s
        sig_s_test = np.array([[[0.52, 0.4206896551724140],
                                [0.696, 0.5172413793103450]],
                               [[0.0, 0.0],
                                [0.696, 0.5172413793103450]]])
        np.testing.assert_array_almost_equal(pydgm.dgm.sig_s_m[0, :, :, :, 0], sig_s_test, 12)

    def test_dgmsolver_homogenize_xs_moments_3(self):
        '''
        Make sure that the cross sections are being properly homogenized
        '''
        self.setGroups(2)
        pydgm.control.dgm_basis_name = 'test/2gdelta'.ljust(256)
        pydgm.control.energy_group_map = [1, 2]
        self.setSolver('fixed')
        pydgm.control.allow_fission = True
        self.setBoundary('reflect')
        pydgm.control.fine_mesh_x = [2, 3, 3, 2]
        pydgm.control.coarse_mesh_x = [0.0, 1.0, 2.0, 4.0, 4.5]
        pydgm.control.material_map = [1, 2, 1, 2]
        pydgm.control.homogenization_map = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        pydgm.state.phi[0, 0, :] = range(1, 11)
        pydgm.state.phi[0, 1, :] = range(10, 0, -1)

        pydgm.dgmsolver.compute_flux_moments()
        pydgm.dgmsolver.compute_xs_moments()

        # Check sig_t
        sig_t_test = np.array([[1.0, 2.4025974025974000],
                               [1.0, 2.2080536912751700]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_sig_t, sig_t_test.T, 12)

        # Check nu_sig_f
        nu_sig_f_test = np.array([[0.2561983471074380, 0.2987012987012990],
                                  [0.3647058823529410, 0.3959731543624160]])
        np.testing.assert_array_almost_equal(pydgm.state.mg_nu_sig_f, nu_sig_f_test.T, 12)

        # Check sig_s
        sig_s_test = np.array([[[0.5438016528925620, 0.4352941176470590],
                                [0.7388429752066120, 0.5435294117647060]],
                               [[0.0000000000000000, 0.0000000000000000],
                                [0.6623376623376620, 0.4872483221476510]]])
        np.testing.assert_array_almost_equal(pydgm.dgm.sig_s_m[0, :, :, :, 0], sig_s_test, 12)

    def test_dgmsolver_non_contiguous(self):
        '''
        Test the 7g->2G, eigenvalue problem on a pin cell of
            water | fuel | water
        with reflective conditions
        '''
        # Set the variables for the test
        self.setGroups(7)
        pydgm.control.energy_group_map = [1, 2, 1, 2, 1, 2, 1]
        pydgm.control.dgm_basis_name = 'test/7g_non_contig'.ljust(256)
        self.setSolver('eigen')
        self.setMesh('coarse_pin')
        self.setBoundary('reflect')
        pydgm.control.material_map = [5, 1, 5]
        pydgm.control.lamb = 0.25

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # set the test flux
        keff_test = 1.0794314789325041
        phi_test = [0.18617101855192203, 2.858915338372074, 1.4772041911943246, 1.0299947729491368, 0.7782291112252604, 0.6601323950057741, 0.0018780861364841711, 0.18615912584783736, 2.8586649211715436, 1.4771766639520822, 1.030040359498237, 0.7782969794725844, 0.6603312122972236, 0.0018857945539742516, 0.18613533094381535, 2.858163988201594, 1.4771216026067822, 1.0301315410919691, 0.7784327301908717, 0.6607289506819793, 0.001901260571677254, 0.1860688679764812, 2.856246121648244, 1.4768054633757053, 1.0308126366153867, 0.7795349485104974, 0.6645605858759833, 0.0020390343478796447, 0.18597801819761287, 2.8534095558345967, 1.4763058823653368, 1.0319062100766097, 0.7813236329806805, 0.6707834262470258, 0.002202198406120643, 0.18591115233580913, 2.851306298580461, 1.4759330573010532, 1.0327026586727457, 0.7826354049117061, 0.6752310599415209, 0.002251216654318464, 0.18586715682184884, 2.8499152893733255, 1.4756853599772022, 1.0332225362074143, 0.7834960048959739, 0.6780933062272468, 0.0022716374303459433, 0.1858453299832966, 2.8492230801887986, 1.475561761882258, 1.0334791905008067, 0.7839221795374745, 0.6794942839316992, 0.002280077669362046, 0.18584532998329656, 2.8492230801887986, 1.475561761882258, 1.0334791905008065, 0.7839221795374745, 0.6794942839316991, 0.0022800776693620455, 0.18586715682184884, 2.8499152893733255, 1.4756853599772024, 1.0332225362074146, 0.7834960048959738, 0.6780933062272467, 0.002271637430345943, 0.18591115233580915, 2.851306298580461, 1.4759330573010532, 1.0327026586727457, 0.7826354049117062, 0.6752310599415207, 0.0022512166543184635, 0.1859780181976129, 2.853409555834596, 1.476305882365337, 1.0319062100766097, 0.7813236329806805, 0.6707834262470258, 0.002202198406120643, 0.1860688679764812, 2.856246121648244, 1.4768054633757055, 1.0308126366153867, 0.7795349485104973, 0.6645605858759831, 0.002039034347879644, 0.18613533094381537, 2.858163988201594, 1.4771216026067824, 1.0301315410919691, 0.7784327301908716, 0.6607289506819792, 0.0019012605716772534, 0.1861591258478374, 2.858664921171543, 1.4771766639520822, 1.0300403594982372, 0.7782969794725842, 0.6603312122972235, 0.0018857945539742511, 0.18617101855192209, 2.8589153383720736, 1.477204191194325, 1.0299947729491368, 0.7782291112252603, 0.660132395005774, 0.0018780861364841707]

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 10)

        # Test the scalar flux
        phi = pydgm.state.phi[0, :, :].flatten('F')
        np.testing.assert_array_almost_equal(phi / phi[0] * phi_test[0], phi_test, 11)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 11)

    def test_dgmsolver_partisn_eigen_2g_l0(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        pydgm.control.fine_mesh_x = [10, 4]
        pydgm.control.coarse_mesh_x = [0.0, 1.5, 2.0]
        pydgm.control.material_map = [1, 5]
        pydgm.control.xs_name = 'test/partisn_cross_sections/anisotropic_2g'.ljust(256)
        pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
        pydgm.control.energy_group_map = [1, 1]
        pydgm.control.angle_order = 8
        pydgm.control.allow_fission = True
        pydgm.control.solver_type = 'eigen'.ljust(256)
        pydgm.control.source_value = 0.0
        self.setBoundary('reflect')
        pydgm.control.scatter_leg_order = 0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux
        phi_test = [[3.442525765957952, 3.44133409525864, 3.438914799438404, 3.435188915015736, 3.4300162013446567, 3.423154461297391, 3.4141703934131375, 3.4022425049312393, 3.3857186894563807, 3.3610957244311783, 3.332547468621578, 3.310828206454775, 3.2983691806875637, 3.292637618967479], [1.038826864565325, 1.0405199414437678, 1.0439340321802706, 1.0491279510472575, 1.0561979892073443, 1.065290252825513, 1.0766260147603826, 1.0905777908540444, 1.1080393189273399, 1.1327704173615665, 1.166565957603695, 1.195247115307628, 1.2108105235380155, 1.2184043154658892]]

        phi_test = np.array(phi_test)

        phi_test = phi_test.reshape(2, pydgm.control.scatter_leg_order + 1, -1)  # Group, legendre, cell

        keff_test = 1.17455939

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        phi_zero = pydgm.state.phi[0, :, :].flatten()

        phi_zero_test = phi_test[:, 0].flatten() / np.linalg.norm(phi_test[:, 0]) * np.linalg.norm(phi_zero)

        np.testing.assert_array_almost_equal(phi_zero, phi_zero_test, 6)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_partisn_eigen_2g_l3(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        pydgm.control.fine_mesh_x = [10, 4]
        pydgm.control.coarse_mesh_x = [0.0, 1.5, 2.0]
        pydgm.control.material_map = [1, 5]
        pydgm.control.xs_name = 'test/partisn_cross_sections/anisotropic_2g'.ljust(256)
        pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
        pydgm.control.energy_group_map = [1, 1]
        pydgm.control.angle_order = 8
        pydgm.control.allow_fission = True
        pydgm.control.solver_type = 'eigen'.ljust(256)
        pydgm.control.source_value = 0.0
        self.setBoundary('reflect')
        pydgm.control.scatter_leg_order = 3
        pydgm.control.lamb = 0.95

        # Partisn output flux
        phi_test = [[[3.4348263649218573, 3.433888018868773, 3.4319780924466303, 3.42902287259914, 3.424889537793379, 3.419345135226939, 3.411967983491092, 3.401955097583459, 3.3876978314964576, 3.3658226138962055, 3.34060976759337, 3.3219476543135085, 3.311461944978981, 3.3067065381042795], [0.0020423376009602104, 0.0061405490727312745, 0.010279647696426843, 0.014487859380892587, 0.01879501657686898, 0.023233575719681245, 0.027840232201383777, 0.03265902220608759, 0.0377496380894604, 0.04322160597649044, 0.040276170715938614, 0.02871879421071569, 0.0172133108882554, 0.005734947202660587], [-0.014080757853872444, -0.013902043581305812, -0.013529929565041343, -0.012931463587873976, -0.012046199898157889, -0.01076583796993369, -0.008890167424784212, -0.006031191544566744, -0.0014017648096517898, 0.006661714787003198, 0.016668552081138488, 0.024174518049647653, 0.028202353769555294, 0.029973018707551896], [-0.0005793248806626183, -0.001756926314379438, -0.002992384144214974, -0.004327832838676431, -0.0058116663533987895, -0.007503402096014022, -0.009482521534408456, -0.011866075285174027, -0.014846832287363936, -0.018786937451990907, -0.018006190583241585, -0.0122930135244824, -0.007176905800153899, -0.0023616380722009875]], [[1.0468914012024944, 1.0481968358689602, 1.0508312357939356, 1.0548444570440296, 1.0603189615576314, 1.0673816455493632, 1.076228676326199, 1.0872017225096173, 1.1011537915124854, 1.1216747771114552, 1.1506436314870738, 1.1750453435123285, 1.1877668049794452, 1.1939304950579657], [-0.0018035802543606028, -0.005420473986754876, -0.009066766225751461, -0.01276274710378097, -0.016529853018089805, -0.020391389910122064, -0.02437367793449243, -0.02850824856871196, -0.032837766571938154, -0.03744058644378857, -0.03479493818294627, -0.02478421594673745, -0.014845697536314062, -0.004944617763983217], [0.009044528296445413, 0.0089941262937423, 0.00888482790544369, 0.008698315780443527, 0.008403457458358271, 0.00795064328003027, 0.0072597762570490235, 0.006182844624800746, 0.004322369521129958, -7.745469082057199e-05, -0.007283839517581971, -0.01236885988414086, -0.013996362056737995, -0.014714527559469726], [0.00015593171761653195, 0.00048010038877656716, 0.000842299907640745, 0.0012717736906895632, 0.0018042482177840942, 0.002486031735562782, 0.003380433007147932, 0.004580592143898934, 0.006250135781847204, 0.008825755375993198, 0.00828387207848599, 0.004886452046255631, 0.0026569024049473873, 0.0008431177342006317]]]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        phi_test = np.array(phi_test)

        phi_test = phi_test.reshape(2, pydgm.control.scatter_leg_order + 1, -1)  # Group, legendre, cell

        keff_test = 1.17563713

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_partisn_eigen_2g_l7_zeroed(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        pydgm.control.fine_mesh_x = [10, 4]
        pydgm.control.coarse_mesh_x = [0.0, 1.5, 2.0]
        pydgm.control.material_map = [1, 5]
        pydgm.control.xs_name = 'test/partisn_cross_sections/anisotropic_2g_zeroed'.ljust(256)
        pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
        pydgm.control.energy_group_map = [1, 1]
        pydgm.control.angle_order = 8
        pydgm.control.allow_fission = True
        pydgm.control.solver_type = 'eigen'.ljust(256)
        pydgm.control.source_value = 0.0
        self.setBoundary('reflect')
        pydgm.control.scatter_leg_order = 7
        pydgm.control.lamb = 1.0

        # Partisn output flux
        phi_test = [[[3.442525765957952, 3.44133409525864, 3.438914799438404, 3.435188915015736, 3.4300162013446567, 3.423154461297391, 3.4141703934131375, 3.4022425049312393, 3.3857186894563807, 3.3610957244311783, 3.332547468621578, 3.310828206454775, 3.2983691806875637, 3.292637618967479], [0.0019644320984535876, 0.0059108120945694995, 0.009910062792966128, 0.013998549920050937, 0.01821447539711394, 0.0225989946277805, 0.02719794108129725, 0.032065052304995886, 0.03727049568899598, 0.04293653815177072, 0.040124283218521156, 0.028601385958514365, 0.017139357954699563, 0.005709715174245851], [-0.012532132606398044, -0.012412411288681507, -0.012159246802683127, -0.011741748785570688, -0.011102896432281906, -0.010139488406617853, -0.008658030296501418, -0.006276951809857101, -0.002206866764278115, 0.005255535093060093, 0.014694305934498608, 0.021718007349751933, 0.02539449632364707, 0.026984954024896868], [-0.00046778165720109954, -0.0014230643907324342, -0.0024386426765394334, -0.0035587633331204543, -0.004834802697643303, -0.006330868937728024, -0.008134119319950651, -0.010375610180247068, -0.013276009498773167, -0.017258163911275617, -0.01664765863491359, -0.01122390121670383, -0.0065043145578594155, -0.0021329570728661276], [0.003969114299288534, 0.00401269078074043, 0.004095196069701726, 0.004205088944363153, 0.004317974960796611, 0.004382969771282358, 0.004292138460096337, 0.0038118805106395898, 0.0024275417388900794, -0.0010155859307936083, -0.005793334371634901, -0.009246181085985392, -0.010849128786682899, -0.01147953358250492], [8.627219578290907e-05, 0.0002714307160306753, 0.0004956786398214036, 0.0007896022697536365, 0.0011920986005699644, 0.0017577114517792342, 0.0025709460150363794, 0.003776204607134917, 0.005643863586461559, 0.008727151896997014, 0.0087004534724765, 0.005368765896173973, 0.002939042494471404, 0.0009374881666138965], [-0.0012338455399673876, -0.0012965906401851829, -0.001422028253820068, -0.0016085775620775788, -0.0018490809840636807, -0.00212121054303277, -0.002365370724816171, -0.002434159103351513, -0.001976610668184789, -0.00016923996766794736, 0.002573819362687621, 0.00449141131591789, 0.005260455272500297, 0.005521341697351342], [1.840769880720461e-05, 4.910755636990116e-05, 6.038798543175905e-05, 3.5299096483823456e-05, -5.088653346535521e-05, -0.00023851493223742137, -0.000599745406981475, -0.0012735717818884024, -0.0025442692239777687, -0.00502646745306673, -0.005168777456609798, -0.0028012837878743507, -0.0013925606361596884, -0.0004220122706306076]], [[1.038826864565325, 1.0405199414437678, 1.0439340321802706, 1.0491279510472575, 1.0561979892073443, 1.065290252825513, 1.0766260147603826, 1.0905777908540444, 1.1080393189273399, 1.1327704173615665, 1.166565957603695, 1.195247115307628, 1.2108105235380155, 1.2184043154658892], [-0.0017407245334155781, -0.005234760773456578, -0.008766789581401696, -0.012362938501971777, -0.016050645928225263, -0.01985945597951201, -0.02382224164936656, -0.027977489969826033, -0.03237537000839117, -0.03710334229483023, -0.034559133368562936, -0.024602951035812462, -0.01473186294651191, -0.004905829460754477], [0.007988002179783696, 0.007960765879538347, 0.007898265607441536, 0.007783087821116828, 0.007585372093529892, 0.007257043348967783, 0.006719774335684138, 0.005827997866319691, 0.004185948821983483, -1.90129809110387e-05, -0.007032887957149146, -0.01191356044176433, -0.013405701553960495, -0.014062567322648795], [0.00011800879780404609, 0.0003659723155822782, 0.0006509752833367376, 0.0010019128678555624, 0.0014547236241962795, 0.0020569208977303036, 0.0028747334190305732, 0.004007351954780396, 0.005632401867932851, 0.00824057743028571, 0.0077964145437174875, 0.004525072515655652, 0.002442683255565622, 0.0007721328099104426], [-0.0008906521221368827, -0.0009365449499154424, -0.0010290223295595993, -0.0011691346663959892, -0.001357481383370794, -0.001592436351699908, -0.0018652704156764746, -0.0021394919429477757, -0.002228893035960515, -0.0009761895052693495, 0.0017006042630191842, 0.003062562168807445, 0.0028818484057990187, 0.0027747808277108488], [3.112628137190779e-05, 9.029048934796821e-05, 0.00013932578157633754, 0.00016839583101848146, 0.0001622621357261038, 9.628165203490191e-05, -7.062050159533859e-05, -0.00041226249765456344, -0.001096598659970919, -0.0027313974690471587, -0.002564785859125975, -0.0008616578944919406, -0.0003363466125526522, -8.528754593967874e-05], [-2.6867653309309292e-05, -6.053675389576518e-06, 3.804812906652369e-05, 0.00011063327980663853, 0.00022012110754064326, 0.0003788015317576568, 0.0006024794524562074, 0.0009003179022477464, 0.0011914241310051858, 0.000697034420395138, -0.000640281151709915, -0.0011056126012183448, -0.0007208905299782367, -0.0005492671454416925], [-2.2772579441603102e-05, -6.869734279097567e-05, -0.00011538022215601754, -0.00016191863663079023, -0.00020475943928101314, -0.00023529998362117194, -0.00023493873533717707, -0.00016063931535125267, 0.00012175371040683974, 0.0012483904597068128, 0.0011309737504319323, 1.678280817822564e-05, -7.189281083687382e-05, -3.563431557253652e-05]]]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # phi_test = np.array([[3.433326, 3.433288, 3.433213, 3.4331, 3.432949, 3.432759, 3.432531, 3.432263, 3.431955, 3.431607, 3.431217, 3.430785, 3.43031, 3.429791, 3.429226, 3.428615, 3.427955, 3.427246, 3.426485, 3.425671, 3.424802, 3.423875, 3.422888, 3.421839, 3.420725, 3.419543, 3.41829, 3.416962, 3.415555, 3.414067, 3.412491, 3.410824, 3.409061, 3.407196, 3.405224, 3.403138, 3.400931, 3.398597, 3.396128, 3.393515, 3.390749, 3.387821, 3.384719, 3.381434, 3.377952, 3.37426, 3.370345, 3.366191, 3.361781, 3.357098, 3.352582, 3.348515, 3.344729, 3.341211, 3.33795, 3.334938, 3.332164, 3.329621, 3.3273, 3.325196, 3.323303, 3.321613, 3.320124, 3.318829, 3.317727, 3.316813, 3.316085, 3.31554, 3.315178, 3.314998, 0.0004094004, 0.001228307, 0.00204753, 0.002867283, 0.003687776, 0.004509223, 0.005331837, 0.006155833, 0.006981427, 0.007808836, 0.00863828, 0.009469979, 0.01030416, 0.01114104, 0.01198085, 0.01282383, 0.01367021, 0.01452023, 0.01537413, 0.01623215, 0.01709456, 0.01796161, 0.01883356, 0.01971069, 0.02059327, 0.0214816, 0.02237596, 0.02327668, 0.02418406, 0.02509845, 0.02602018, 0.02694963, 0.02788717, 0.0288332, 0.02978816, 0.03075248, 0.03172665, 0.03271118, 0.03370661, 0.03471354, 0.0357326, 0.03676448, 0.03780992, 0.03886974, 0.03994483, 0.04103617, 0.04214482, 0.043272, 0.044419, 0.0455873, 0.04501365, 0.04268848, 0.04036613, 0.03804639, 0.03572907, 0.033414, 0.03110099, 0.02878989, 0.02648052, 0.02417273, 0.02186636, 0.01956128, 0.01725733, 0.01495437, 0.01265226, 0.01035088, 0.00805008, 0.005749734, 0.003449712, 0.001149882], [1.04734, 1.04739, 1.047492, 1.047644, 1.047847, 1.048102, 1.048407, 1.048764, 1.049173, 1.049633, 1.050146, 1.050712, 1.05133, 1.052002, 1.052729, 1.05351, 1.054346, 1.055239, 1.056188, 1.057196, 1.058262, 1.059389, 1.060577, 1.061828, 1.063143, 1.064525, 1.065976, 1.067497, 1.069091, 1.070762, 1.072512, 1.074346, 1.076267, 1.078281, 1.080392, 1.082607, 1.084933, 1.087377, 1.08995, 1.09266, 1.09552, 1.098544, 1.101747, 1.105145, 1.10876, 1.112615, 1.116735, 1.121151, 1.125898, 1.131015, 1.137325, 1.144257, 1.150486, 1.156095, 1.161153, 1.165716, 1.169832, 1.17354, 1.176872, 1.179856, 1.182513, 1.184862, 1.186919, 1.188695, 1.1902, 1.191444, 1.192431, 1.193168, 1.193657, 1.193901, -0.0003617221, -0.001085242, -0.00180899, -0.002533119, -0.003257779, -0.003983126, -0.004709312, -0.005436491, -0.00616482, -0.006894453, -0.007625549, -0.008358266, -0.009092764, -0.009829207, -0.01056776, -0.01130858, -0.01205185, -0.01279773, -0.0135464, -0.01429804, -0.01505283, -0.01581094, -0.01657259, -0.01733795, -0.01810722, -0.01888063, -0.01965837, -0.02044067, -0.02122776, -0.02201987, -0.02281726, -0.02362018, -0.02442892, -0.02524375, -0.02606498, -0.02689293, -0.02772795, -0.0285704, -0.02942068, -0.0302792, -0.03114642, -0.03202284, -0.03290899, -0.03380545, -0.03471287, -0.03563194, -0.03656344, -0.03750822, -0.03846724, -0.03944153, -0.03892121, -0.03690057, -0.0348842, -0.03287175, -0.03086291, -0.02885737, -0.02685485, -0.0248551, -0.02285785, -0.02086288, -0.01886996, -0.01687886, -0.01488938, -0.01290132, -0.01091447, -0.008928642, -0.006943643, -0.004959288, -0.00297539, -0.0009917663]])
        phi_test = np.array(phi_test)

        phi_test = phi_test.reshape(2, pydgm.control.scatter_leg_order + 1, -1)  # Group, legendre, cell

        keff_test = 1.17455939

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def test_dgmsolver_partisn_eigen_2g_l7_symmetric(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        pydgm.control.fine_mesh_x = [10, 4]
        pydgm.control.coarse_mesh_x = [0.0, 1.5, 2.0]
        pydgm.control.material_map = [1, 5]
        pydgm.control.xs_name = 'test/partisn_cross_sections/anisotropic_2g_symmetric'.ljust(256)
        pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
        pydgm.control.energy_group_map = [1, 1]
        pydgm.control.angle_order = 8
        pydgm.control.allow_fission = True
        pydgm.control.solver_type = 'eigen'.ljust(256)
        pydgm.control.source_value = 0.0
        self.setBoundary('reflect')
        pydgm.control.scatter_leg_order = 7
        pydgm.control.lamb = 1.0

        # Partisn output flux
        phi_test = [[[0.1538782092306766, 0.15382581211270707, 0.15371986228765858, 0.153557761213616, 0.15333472881184002, 0.15304218023034566, 0.15266423446037952, 0.1521701827407139, 0.15149814229420455, 0.1505194051927887, 0.1494249687053612, 0.1486226070725345, 0.14817047331310246, 0.14796502736009512], [0.0001026884291694685, 0.000308030321038727, 0.0005132665423330503, 0.0007183238836813465, 0.0009231242116952735, 0.0011275804740904216, 0.001331589291639088, 0.0015350161940947502, 0.0017376649215678002, 0.0019392120261786507, 0.0017831926104664695, 0.0012716369586346283, 0.0007622344671049473, 0.00025396061625605824], [-0.000682002429319776, -0.0006703722551940497, -0.0006465291239265841, -0.0006091636714206919, -0.0005558703969694842, -0.00048233555403088147, -0.0003805905629842574, -0.00023524453134053137, -1.530782750082567e-05, 0.000343640189869052, 0.0007749990633443837, 0.0010955352332986893, 0.00126790980764641, 0.0013438061833929496], [-3.058337499400269e-05, -9.237270549150144e-05, -0.000156061628751189, -0.00022303056882785367, -0.0002948629752353676, -0.0003735095105970188, -0.00046159206220763036, -0.0005630090779214299, -0.0006841935938615459, -0.0008367925438085822, -0.0007896375192952836, -0.0005397705453395623, -0.00031536355653434935, -0.00010380975887062981], [0.00023192773237918404, 0.00023170419605027595, 0.00023099437633635964, 0.00022917428036478126, 0.00022500268466479033, 0.00021605146985450782, 0.000197467460152566, 0.00015928145031182932, 8.053932401339784e-05, -8.35365504396621e-05, -0.0002985310711184743, -0.00045360492028924913, -0.0005279989261356239, -0.0005580164988029952], [7.399667935943047e-06, 2.2713517743269424e-05, 3.961572529958277e-05, 5.932811702596529e-05, 8.337219672099492e-05, 0.00011383325722981018, 0.00015386938501401595, 0.00020875066014553042, 0.0002880504099107323, 0.0004103501289148088, 0.00039931287995456297, 0.0002511676906294287, 0.00013917831523372736, 4.4655208369662885e-05], [-7.735314258768304e-05, -7.939037040513011e-05, -8.340114274570012e-05, -8.919024664814186e-05, -9.625067330982931e-05, -0.00010335265393286459, -0.00010763270188858098, -0.00010258629461190995, -7.365082975850298e-05, 1.1510318766527229e-05, 0.0001330732285196889, 0.00021783037521026132, 0.00025313880126033583, 0.0002655853959215326], [-6.052281039214784e-07, -2.105593440887652e-06, -4.518823271217054e-06, -8.613917736378408e-06, -1.546882765090553e-05, -2.6773569766345116e-05, -4.5441298246425184e-05, -7.689028022185053e-05, -0.0001317898459288181, -0.00023200916513577488, -0.0002324970071112759, -0.00012949718930364363, -6.569369965651493e-05, -2.012501435494406e-05]], [[0.15387820923067544, 0.15382581211270596, 0.1537198622876574, 0.15355776121361495, 0.1533347288118389, 0.15304218023034463, 0.15266423446037858, 0.152170182740713, 0.1514981422942038, 0.15051940519278806, 0.14942496870536068, 0.14862260707253408, 0.1481704733131023, 0.14796502736009523], [0.00010268842916943727, 0.000308030321038652, 0.0005132665423329395, 0.0007183238836811969, 0.0009231242116950705, 0.0011275804740901753, 0.0013315892916388105, 0.0015350161940944143, 0.0017376649215673982, 0.001939212026178192, 0.0017831926104659298, 0.0012716369586340077, 0.0007622344671042425, 0.0002539606162552429], [-0.0006820024293195696, -0.0006703722551938442, -0.0006465291239263751, -0.0006091636714204733, -0.0005558703969692639, -0.0004823355540306568, -0.0003805905629840232, -0.00023524453134028678, -1.5307827500579338e-05, 0.00034364018986930527, 0.0007749990633446344, 0.001095535233298939, 0.001267909807646645, 0.0013438061833931413], [-3.058337499400052e-05, -9.237270549149494e-05, -0.00015606162875118554, -0.00022303056882785324, -0.0002948629752353676, -0.0003735095105970119, -0.00046159206220760824, -0.0005630090779214117, -0.0006841935938615164, -0.0008367925438085419, -0.0007896375192952203, -0.0005397705453394808, -0.00031536355653423464, -0.00010380975887046675], [0.00023192773237917623, 0.00023170419605026988, 0.0002309943763363501, 0.00022917428036476999, 0.00022500268466477298, 0.00021605146985448354, 0.00019746746015253044, 0.00015928145031178682, 8.05393240133484e-05, -8.353655043972022e-05, -0.00029853107111854366, -0.00045360492028932026, -0.0005279989261356959, -0.0005580164988030507], [7.399667935945216e-06, 2.2713517743276363e-05, 3.961572529959361e-05, 5.932811702597917e-05, 8.337219672100403e-05, 0.00011383325722982016, 0.00015386938501402853, 0.00020875066014554213, 0.00028805040991074357, 0.0004103501289148127, 0.0003993128799545595, 0.0002511676906294157, 0.00013917831523369874, 4.46552083696e-05], [-7.735314258769258e-05, -7.939037040514269e-05, -8.340114274571009e-05, -8.91902466481514e-05, -9.625067330983582e-05, -0.00010335265393286676, -0.00010763270188857924, -0.00010258629461190822, -7.365082975849735e-05, 1.151031876654024e-05, 0.0001330732285197123, 0.00021783037521029254, 0.00025313880126037183, 0.0002655853959215638], [-6.052281039223457e-07, -2.105593440891989e-06, -4.518823271223559e-06, -8.613917736386215e-06, -1.5468827650912467e-05, -2.6773569766352055e-05, -4.544129824643039e-05, -7.689028022185747e-05, -0.00013178984592882633, -0.00023200916513578225, -0.00023249700711128326, -0.0001294971893036471, -6.569369965651146e-05, -2.0125014354917172e-05]]]

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # phi_test = np.array([[3.433326, 3.433288, 3.433213, 3.4331, 3.432949, 3.432759, 3.432531, 3.432263, 3.431955, 3.431607, 3.431217, 3.430785, 3.43031, 3.429791, 3.429226, 3.428615, 3.427955, 3.427246, 3.426485, 3.425671, 3.424802, 3.423875, 3.422888, 3.421839, 3.420725, 3.419543, 3.41829, 3.416962, 3.415555, 3.414067, 3.412491, 3.410824, 3.409061, 3.407196, 3.405224, 3.403138, 3.400931, 3.398597, 3.396128, 3.393515, 3.390749, 3.387821, 3.384719, 3.381434, 3.377952, 3.37426, 3.370345, 3.366191, 3.361781, 3.357098, 3.352582, 3.348515, 3.344729, 3.341211, 3.33795, 3.334938, 3.332164, 3.329621, 3.3273, 3.325196, 3.323303, 3.321613, 3.320124, 3.318829, 3.317727, 3.316813, 3.316085, 3.31554, 3.315178, 3.314998, 0.0004094004, 0.001228307, 0.00204753, 0.002867283, 0.003687776, 0.004509223, 0.005331837, 0.006155833, 0.006981427, 0.007808836, 0.00863828, 0.009469979, 0.01030416, 0.01114104, 0.01198085, 0.01282383, 0.01367021, 0.01452023, 0.01537413, 0.01623215, 0.01709456, 0.01796161, 0.01883356, 0.01971069, 0.02059327, 0.0214816, 0.02237596, 0.02327668, 0.02418406, 0.02509845, 0.02602018, 0.02694963, 0.02788717, 0.0288332, 0.02978816, 0.03075248, 0.03172665, 0.03271118, 0.03370661, 0.03471354, 0.0357326, 0.03676448, 0.03780992, 0.03886974, 0.03994483, 0.04103617, 0.04214482, 0.043272, 0.044419, 0.0455873, 0.04501365, 0.04268848, 0.04036613, 0.03804639, 0.03572907, 0.033414, 0.03110099, 0.02878989, 0.02648052, 0.02417273, 0.02186636, 0.01956128, 0.01725733, 0.01495437, 0.01265226, 0.01035088, 0.00805008, 0.005749734, 0.003449712, 0.001149882], [1.04734, 1.04739, 1.047492, 1.047644, 1.047847, 1.048102, 1.048407, 1.048764, 1.049173, 1.049633, 1.050146, 1.050712, 1.05133, 1.052002, 1.052729, 1.05351, 1.054346, 1.055239, 1.056188, 1.057196, 1.058262, 1.059389, 1.060577, 1.061828, 1.063143, 1.064525, 1.065976, 1.067497, 1.069091, 1.070762, 1.072512, 1.074346, 1.076267, 1.078281, 1.080392, 1.082607, 1.084933, 1.087377, 1.08995, 1.09266, 1.09552, 1.098544, 1.101747, 1.105145, 1.10876, 1.112615, 1.116735, 1.121151, 1.125898, 1.131015, 1.137325, 1.144257, 1.150486, 1.156095, 1.161153, 1.165716, 1.169832, 1.17354, 1.176872, 1.179856, 1.182513, 1.184862, 1.186919, 1.188695, 1.1902, 1.191444, 1.192431, 1.193168, 1.193657, 1.193901, -0.0003617221, -0.001085242, -0.00180899, -0.002533119, -0.003257779, -0.003983126, -0.004709312, -0.005436491, -0.00616482, -0.006894453, -0.007625549, -0.008358266, -0.009092764, -0.009829207, -0.01056776, -0.01130858, -0.01205185, -0.01279773, -0.0135464, -0.01429804, -0.01505283, -0.01581094, -0.01657259, -0.01733795, -0.01810722, -0.01888063, -0.01965837, -0.02044067, -0.02122776, -0.02201987, -0.02281726, -0.02362018, -0.02442892, -0.02524375, -0.02606498, -0.02689293, -0.02772795, -0.0285704, -0.02942068, -0.0302792, -0.03114642, -0.03202284, -0.03290899, -0.03380545, -0.03471287, -0.03563194, -0.03656344, -0.03750822, -0.03846724, -0.03944153, -0.03892121, -0.03690057, -0.0348842, -0.03287175, -0.03086291, -0.02885737, -0.02685485, -0.0248551, -0.02285785, -0.02086288, -0.01886996, -0.01687886, -0.01488938, -0.01290132, -0.01091447, -0.008928642, -0.006943643, -0.004959288, -0.00297539, -0.0009917663]])
        phi_test = np.array(phi_test)

        phi_test = phi_test.reshape(2, pydgm.control.scatter_leg_order + 1, -1)  # Group, legendre, cell

        keff_test = 0.15282105

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 12)

        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_fine_groups, pydgm.control.number_cells))
        for c in range(pydgm.control.number_cells):
            for a in range(nAngles):
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, a, c]
                phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, 2 * nAngles - a - 1, c]
        np.testing.assert_array_almost_equal(pydgm.state.phi[0, :, :], phi_test, 12)

    def tearDown(self):
        pydgm.dgmsolver.finalize_dgmsolver()
        pydgm.control.finalize_control()


class TestDGMSOLVER_2D(unittest.TestCase):

    def setUp(self):
        # Set the variables for the test
        pydgm.control.spatial_dimension = 2
        pydgm.control.angle_order = 8
        pydgm.control.angle_option = pydgm.angle.gl
        pydgm.control.recon_print = False
        pydgm.control.eigen_print = False
        pydgm.control.outer_print = False
        pydgm.control.recon_tolerance = 1e-14
        pydgm.control.eigen_tolerance = 1e-14
        pydgm.control.outer_tolerance = 1e-15
        pydgm.control.scatter_leg_order = 0
        pydgm.control.equation_type = 'DD'
        pydgm.control.use_dgm = True
        pydgm.control.store_psi = True
        pydgm.control.ignore_warnings = True
        pydgm.control.lamb = 1.0
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 0.0
        pydgm.control.boundary_south = 0.0

    def tearDown(self):
        pydgm.dgmsolver.finalize_dgmsolver()
        pydgm.control.finalize_control()

    def setGroups(self, G):
        if G == 1:
            pydgm.control.xs_name = 'test/1gXS.anlxs'.ljust(256)
            pydgm.control.dgm_basis_name = 'test/1gbasis'.ljust(256)
            pydgm.control.energy_group_map = [1]
        if G == 2:
            pydgm.control.xs_name = 'test/2gXS.anlxs'.ljust(256)
            pydgm.control.dgm_basis_name = 'test/2gbasis'.ljust(256)
            pydgm.control.energy_group_map = [1, 1]
        elif G == 4:
            pydgm.control.xs_name = 'test/4gXS.anlxs'.ljust(256)
            pydgm.control.energy_group_map = [1, 1, 2, 2]
            pydgm.control.dgm_basis_name = 'test/4gbasis'.ljust(256)
        elif G == 7:
            pydgm.control.xs_name = 'test/7gXS.anlxs'.ljust(256)
            pydgm.control.dgm_basis_name = 'test/7gbasis'.ljust(256)
            pydgm.control.energy_group_map = [1, 1, 1, 1, 2, 2, 2]

    def setSolver(self, solver):
        if solver == 'fixed':
            pydgm.control.solver_type = 'fixed'.ljust(256)
            pydgm.control.source_value = 1.0
            pydgm.control.allow_fission = False
            pydgm.control.max_recon_iters = 10000
            pydgm.control.max_eigen_iters = 1
            pydgm.control.max_outer_iters = 100000
        elif solver == 'eigen':
            pydgm.control.solver_type = 'eigen'.ljust(256)
            pydgm.control.source_value = 0.0
            pydgm.control.allow_fission = True
            pydgm.control.max_recon_iters = 10000
            pydgm.control.max_eigen_iters = 10000
            pydgm.control.max_outer_iters = 1000

    def tearDown(self):
        pydgm.solver.finalize_solver()
        pydgm.control.finalize_control()

    def angular_test(self):
        # Test the angular flux
        nAngles = pydgm.control.number_angles
        phi_test = np.zeros((pydgm.control.number_groups, pydgm.control.number_cells))
        for o in range(4):
            for c in range(pydgm.control.number_cells):
                for a in range(nAngles):
                    phi_test[:, c] += pydgm.angle.wt[a] * pydgm.state.psi[:, o * nAngles + a, c]
        np.testing.assert_array_almost_equal(phi_test, pydgm.state.phi[0, :, :], 12)

    def set_mesh(self, pType):
        '''Select the problem mesh'''

        if pType == 'homogeneous':
            pydgm.control.fine_mesh_x = [10]
            pydgm.control.fine_mesh_y = [10]
            pydgm.control.coarse_mesh_x = [0.0, 100000.0]
            pydgm.control.coarse_mesh_y = [0.0, 100000.0]
            pydgm.control.material_map = [2]
            pydgm.control.boundary_east = 1.0
            pydgm.control.boundary_west = 1.0
            pydgm.control.boundary_north = 1.0
            pydgm.control.boundary_south = 1.0
        elif pType == 'simple':
            pydgm.control.fine_mesh_x = [25]
            pydgm.control.fine_mesh_y = [25]
            pydgm.control.coarse_mesh_x = [0.0, 10.0]
            pydgm.control.coarse_mesh_y = [0.0, 10.0]
            pydgm.control.material_map = [1]
        elif pType == 'slab':
            pydgm.control.fine_mesh_x = [10]
            pydgm.control.fine_mesh_y = [20]
            pydgm.control.coarse_mesh_x = [0.0, 21.42]
            pydgm.control.coarse_mesh_y = [0.0, 21.42]
            pydgm.control.material_map = [2]
        elif pType == 'c5g7':
            pydgm.control.fine_mesh_x = [10, 10, 6]
            pydgm.control.fine_mesh_y = [10, 10, 6]
            pydgm.control.coarse_mesh_x = [0.0, 21.42, 42.84, 64.26]
            pydgm.control.coarse_mesh_y = [0.0, 21.42, 42.84, 64.26]
            pydgm.control.material_map = [2, 4, 5,
                                          4, 2, 5,
                                          5, 5, 5]
        elif pType == 'single':
            pydgm.control.fine_mesh_x = [2]
            pydgm.control.fine_mesh_y = [1]
            pydgm.control.coarse_mesh_x = [0.0, 1.0]
            pydgm.control.coarse_mesh_y = [0.0, 1.0]
            pydgm.control.material_map = [1]

    def test_solver_basic_2D_1g_reflect(self):
        '''
        Test for a basic 1 group problem
        '''
        self.setSolver('fixed')
        self.set_mesh('homogeneous')
        self.setGroups(1)
        pydgm.control.angle_order = 8

        pydgm.control.allow_fission = False

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 1)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [5] * 100

        phi_test = np.array(phi_test)

        # Test the scalar flux
        phi = pydgm.state.mg_phi[0, :, :].flatten()
        np.testing.assert_array_almost_equal(phi, phi_test, 8)

        self.angular_test()

    def test_solver_basic_2D_1g_1a_vacuum(self):
        '''
        Test for a basic 1 group problem
        '''
        self.set_mesh('simple')
        pydgm.control.xs_name = 'test/1gXS.anlxs'.ljust(256)
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 0.0
        pydgm.control.boundary_south = 0.0
        pydgm.control.allow_fission = False

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 1)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[0.5128609747568281, 0.6773167712139831, 0.7428920389440171, 0.7815532843645795, 0.8017050988344507, 0.8129183924456294, 0.8186192333777655, 0.8218872988327544, 0.8235294558562516, 0.8244499117457011, 0.8249136380974397, 0.8251380055566573, 0.8252036667060597, 0.8251380055566576, 0.8249136380974401, 0.8244499117457017, 0.8235294558562521, 0.8218872988327554, 0.8186192333777662, 0.81291839244563, 0.8017050988344515, 0.7815532843645803, 0.7428920389440175, 0.6773167712139835, 0.5128609747568282, 0.6773167712139831, 0.9191522109956556, 1.0101279836265808, 1.046811188269745, 1.0706509901493697, 1.082306179953408, 1.0890982284197688, 1.092393940905045, 1.0943710244790774, 1.095322191522249, 1.0958571613995292, 1.0961001761636988, 1.0961736115735345, 1.0961001761636997, 1.0958571613995298, 1.0953221915222502, 1.094371024479079, 1.092393940905046, 1.08909822841977, 1.082306179953409, 1.0706509901493706, 1.046811188269746, 1.0101279836265817, 0.9191522109956564, 0.6773167712139837, 0.742892038944017, 1.010127983626581, 1.1482625986461896, 1.1962723842001344, 1.2162573092331372, 1.2309663391416374, 1.2373535288720443, 1.2414786838078147, 1.2432965986450648, 1.2444791104681647, 1.24499985971512, 1.2452803731491178, 1.2453559925876914, 1.2452803731491184, 1.244999859715121, 1.244479110468166, 1.2432965986450666, 1.2414786838078167, 1.237353528872046, 1.230966339141639, 1.2162573092331381, 1.1962723842001353, 1.1482625986461907, 1.010127983626582, 0.7428920389440178, 0.7815532843645796, 1.046811188269745, 1.196272384200134, 1.2752422132283252, 1.2995505587401641, 1.310409682796424, 1.3196712848467558, 1.3229121459817077, 1.3255006837110048, 1.3264359863630988, 1.3271401701539467, 1.3273900240538614, 1.3274869234142137, 1.327390024053862, 1.3271401701539483, 1.3264359863631008, 1.3255006837110068, 1.3229121459817097, 1.3196712848467576, 1.3104096827964256, 1.2995505587401661, 1.275242213228327, 1.1962723842001357, 1.0468111882697462, 0.7815532843645802, 0.8017050988344504, 1.0706509901493695, 1.2162573092331366, 1.2995505587401643, 1.3452497209031955, 1.3567411771030033, 1.3627115460270347, 1.3687134641761085, 1.3700956107492908, 1.3718153695089819, 1.3722188033283726, 1.3726261825701194, 1.3726746849086748, 1.3726261825701203, 1.3722188033283742, 1.3718153695089843, 1.3700956107492925, 1.3687134641761105, 1.3627115460270367, 1.356741177103005, 1.3452497209031975, 1.2995505587401661, 1.2162573092331384, 1.0706509901493706, 0.8017050988344514, 0.8129183924456289, 1.0823061799534075, 1.2309663391416374, 1.3104096827964238, 1.3567411771030033, 1.3837407849220562, 1.3883940252403495, 1.391781180853413, 1.3958074539475693, 1.3960964469643635, 1.3973279212330587, 1.3973887886413996, 1.3976146226859119, 1.3973887886414005, 1.3973279212330607, 1.3960964469643657, 1.3958074539475707, 1.3917811808534148, 1.3883940252403517, 1.3837407849220587, 1.3567411771030051, 1.3104096827964258, 1.2309663391416386, 1.0823061799534086, 0.81291839244563, 0.8186192333777653, 1.0890982284197686, 1.2373535288720436, 1.319671284846756, 1.3627115460270351, 1.3883940252403497, 1.4048482432271674, 1.4059080588108543, 1.4079482979581446, 1.4107567935223844, 1.4103944840640301, 1.4113681192038354, 1.4110951509099934, 1.411368119203836, 1.4103944840640317, 1.4107567935223853, 1.4079482979581461, 1.4059080588108563, 1.4048482432271694, 1.3883940252403517, 1.362711546027037, 1.3196712848467576, 1.237353528872046, 1.0890982284197699, 0.8186192333777663, 0.8218872988327544, 1.092393940905045, 1.2414786838078145, 1.322912145981707, 1.3687134641761085, 1.3917811808534124, 1.4059080588108548, 1.4163858413766799, 1.4155936684368302, 1.4169325249341456, 1.4189994578626368, 1.4181484360902454, 1.4191873654776683, 1.4181484360902463, 1.4189994578626375, 1.4169325249341471, 1.415593668436832, 1.416385841376682, 1.4059080588108568, 1.3917811808534146, 1.3687134641761105, 1.3229121459817095, 1.2414786838078165, 1.092393940905047, 0.8218872988327552, 0.8235294558562515, 1.0943710244790772, 1.2432965986450644, 1.325500683711004, 1.3700956107492905, 1.3958074539475689, 1.4079482979581444, 1.4155936684368298, 1.4226595845322698, 1.4209588928818724, 1.421835104078357, 1.423671773688655, 1.4219795630324892, 1.423671773688656, 1.4218351040783586, 1.420958892881874, 1.4226595845322718, 1.4155936684368327, 1.4079482979581466, 1.3958074539475707, 1.3700956107492928, 1.3255006837110068, 1.2432965986450666, 1.0943710244790792, 0.8235294558562524, 0.8244499117457008, 1.0953221915222489, 1.2444791104681645, 1.3264359863630988, 1.3718153695089823, 1.396096446964363, 1.4107567935223833, 1.4169325249341451, 1.4209588928818722, 1.4259745842172793, 1.424082580661134, 1.4241542494391093, 1.4264775572959318, 1.42415424943911, 1.4240825806611355, 1.425974584217281, 1.420958892881874, 1.4169325249341471, 1.4107567935223857, 1.3960964469643653, 1.3718153695089845, 1.3264359863631006, 1.2444791104681667, 1.0953221915222502, 0.824449911745702, 0.8249136380974391, 1.0958571613995285, 1.2449998597151197, 1.3271401701539467, 1.3722188033283722, 1.3973279212330585, 1.4103944840640301, 1.4189994578626361, 1.4218351040783568, 1.4240825806611341, 1.427381093837987, 1.426071570295947, 1.4256483954611119, 1.4260715702959486, 1.4273810938379876, 1.424082580661136, 1.4218351040783581, 1.4189994578626381, 1.410394484064032, 1.3973279212330605, 1.3722188033283746, 1.3271401701539485, 1.2449998597151215, 1.0958571613995303, 0.8249136380974402, 0.8251380055566571, 1.0961001761636986, 1.2452803731491175, 1.3273900240538605, 1.3726261825701191, 1.3973887886413991, 1.4113681192038343, 1.4181484360902443, 1.4236717736886548, 1.4241542494391093, 1.4260715702959472, 1.4284214388119818, 1.425280452566786, 1.428421438811983, 1.426071570295949, 1.4241542494391097, 1.4236717736886555, 1.4181484360902465, 1.4113681192038365, 1.3973887886414016, 1.3726261825701216, 1.3273900240538627, 1.2452803731491189, 1.0961001761637001, 0.825138005556658, 0.8252036667060596, 1.0961736115735343, 1.2453559925876905, 1.3274869234142128, 1.3726746849086742, 1.3976146226859112, 1.4110951509099916, 1.4191873654776679, 1.421979563032488, 1.4264775572959316, 1.4256483954611114, 1.4252804525667855, 1.4309739984926175, 1.4252804525667866, 1.4256483954611128, 1.4264775572959327, 1.4219795630324894, 1.4191873654776692, 1.4110951509099945, 1.3976146226859132, 1.3726746849086764, 1.327486923414215, 1.2453559925876925, 1.0961736115735354, 0.8252036667060605, 0.825138005556657, 1.0961001761636986, 1.2452803731491173, 1.3273900240538608, 1.372626182570119, 1.3973887886413987, 1.4113681192038343, 1.4181484360902448, 1.4236717736886546, 1.4241542494391095, 1.426071570295948, 1.428421438811982, 1.4252804525667868, 1.4284214388119838, 1.426071570295949, 1.4241542494391108, 1.4236717736886564, 1.418148436090247, 1.411368119203837, 1.3973887886414011, 1.3726261825701218, 1.3273900240538627, 1.2452803731491195, 1.0961001761637001, 0.8251380055566581, 0.8249136380974397, 1.095857161399529, 1.24499985971512, 1.3271401701539465, 1.3722188033283722, 1.3973279212330587, 1.4103944840640301, 1.418999457862636, 1.4218351040783574, 1.4240825806611341, 1.427381093837987, 1.4260715702959483, 1.4256483954611125, 1.4260715702959488, 1.4273810938379878, 1.4240825806611361, 1.421835104078359, 1.4189994578626386, 1.4103944840640321, 1.3973279212330607, 1.3722188033283749, 1.3271401701539487, 1.2449998597151215, 1.0958571613995305, 0.8249136380974409, 0.8244499117457011, 1.0953221915222489, 1.2444791104681645, 1.3264359863630988, 1.3718153695089828, 1.3960964469643642, 1.410756793522384, 1.4169325249341456, 1.420958892881872, 1.4259745842172795, 1.4240825806611346, 1.4241542494391095, 1.426477557295932, 1.4241542494391102, 1.4240825806611361, 1.4259745842172817, 1.4209588928818744, 1.4169325249341482, 1.4107567935223861, 1.3960964469643657, 1.371815369508985, 1.326435986363101, 1.2444791104681663, 1.0953221915222509, 0.8244499117457021, 0.8235294558562516, 1.0943710244790774, 1.2432965986450648, 1.325500683711005, 1.3700956107492908, 1.3958074539475689, 1.4079482979581448, 1.4155936684368302, 1.4226595845322698, 1.4209588928818724, 1.421835104078357, 1.423671773688655, 1.4219795630324894, 1.4236717736886562, 1.4218351040783583, 1.420958892881874, 1.422659584532272, 1.4155936684368329, 1.4079482979581472, 1.3958074539475713, 1.3700956107492932, 1.3255006837110068, 1.2432965986450673, 1.0943710244790794, 0.8235294558562526, 0.8218872988327546, 1.0923939409050452, 1.241478683807815, 1.3229121459817077, 1.368713464176108, 1.3917811808534133, 1.4059080588108555, 1.4163858413766814, 1.4155936684368304, 1.4169325249341456, 1.4189994578626364, 1.4181484360902452, 1.4191873654776685, 1.4181484360902465, 1.4189994578626381, 1.4169325249341473, 1.4155936684368324, 1.4163858413766832, 1.4059080588108572, 1.3917811808534155, 1.3687134641761114, 1.32291214598171, 1.2414786838078167, 1.0923939409050465, 0.8218872988327557, 0.8186192333777654, 1.089098228419769, 1.2373535288720448, 1.3196712848467562, 1.3627115460270354, 1.3883940252403495, 1.4048482432271683, 1.4059080588108557, 1.4079482979581455, 1.410756793522384, 1.4103944840640303, 1.4113681192038354, 1.411095150909993, 1.411368119203836, 1.410394484064032, 1.410756793522386, 1.4079482979581472, 1.4059080588108572, 1.4048482432271705, 1.388394025240352, 1.3627115460270374, 1.3196712848467584, 1.237353528872046, 1.0890982284197708, 0.8186192333777667, 0.8129183924456292, 1.0823061799534082, 1.2309663391416377, 1.3104096827964242, 1.3567411771030033, 1.3837407849220569, 1.3883940252403497, 1.391781180853413, 1.3958074539475698, 1.3960964469643644, 1.3973279212330594, 1.3973887886413998, 1.397614622685912, 1.3973887886414005, 1.3973279212330607, 1.396096446964366, 1.3958074539475713, 1.391781180853415, 1.388394025240352, 1.3837407849220584, 1.3567411771030051, 1.310409682796426, 1.2309663391416392, 1.0823061799534093, 0.8129183924456299, 0.8017050988344508, 1.07065099014937, 1.2162573092331375, 1.2995505587401643, 1.3452497209031953, 1.3567411771030036, 1.3627115460270354, 1.3687134641761085, 1.370095610749291, 1.3718153695089825, 1.3722188033283735, 1.3726261825701203, 1.372674684908675, 1.3726261825701211, 1.3722188033283742, 1.371815369508985, 1.3700956107492934, 1.3687134641761116, 1.3627115460270374, 1.3567411771030051, 1.3452497209031975, 1.2995505587401661, 1.2162573092331384, 1.0706509901493708, 0.8017050988344514, 0.7815532843645797, 1.046811188269745, 1.1962723842001342, 1.2752422132283254, 1.2995505587401648, 1.3104096827964244, 1.3196712848467562, 1.322912145981708, 1.3255006837110048, 1.3264359863630992, 1.3271401701539476, 1.3273900240538619, 1.3274869234142137, 1.327390024053862, 1.3271401701539485, 1.3264359863631006, 1.3255006837110068, 1.3229121459817104, 1.3196712848467584, 1.3104096827964262, 1.2995505587401661, 1.2752422132283268, 1.1962723842001353, 1.0468111882697464, 0.7815532843645804, 0.742892038944017, 1.0101279836265813, 1.1482625986461896, 1.196272384200134, 1.2162573092331368, 1.2309663391416377, 1.2373535288720443, 1.241478683807815, 1.2432965986450653, 1.2444791104681654, 1.2449998597151208, 1.245280373149118, 1.2453559925876916, 1.245280373149119, 1.2449998597151217, 1.2444791104681663, 1.2432965986450666, 1.2414786838078173, 1.2373535288720463, 1.230966339141639, 1.2162573092331386, 1.1962723842001357, 1.1482625986461912, 1.0101279836265824, 0.7428920389440179, 0.677316771213983, 0.9191522109956558, 1.010127983626581, 1.0468111882697448, 1.0706509901493695, 1.0823061799534077, 1.0890982284197688, 1.0923939409050452, 1.0943710244790776, 1.0953221915222493, 1.0958571613995294, 1.096100176163699, 1.0961736115735348, 1.0961001761636995, 1.09585716139953, 1.0953221915222504, 1.0943710244790792, 1.092393940905047, 1.0890982284197708, 1.0823061799534093, 1.0706509901493708, 1.0468111882697464, 1.010127983626582, 0.9191522109956568, 0.6773167712139838, 0.5128609747568279, 0.6773167712139831, 0.7428920389440171, 0.7815532843645797, 0.8017050988344507, 0.8129183924456291, 0.8186192333777655, 0.8218872988327544, 0.8235294558562514, 0.8244499117457011, 0.8249136380974398, 0.8251380055566575, 0.82520366670606, 0.8251380055566576, 0.8249136380974401, 0.8244499117457018, 0.8235294558562525, 0.8218872988327557, 0.8186192333777665, 0.8129183924456304, 0.8017050988344514, 0.7815532843645805, 0.7428920389440181, 0.6773167712139839, 0.5128609747568283]]]

        phi_test = np.array(phi_test)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten()
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()

    def test_solver_basic_2D_1g_1a_vacuum_l1(self):
        '''
        Test for a basic 1 group problem
        '''
        self.set_mesh('simple')
        pydgm.control.material_map = [2]
        pydgm.control.xs_name = 'test/1gXS.anlxs'.ljust(256)
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 1.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0
        pydgm.control.allow_fission = False
        pydgm.control.scatter_leg_order = 1

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 1)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[2.1155214619699514, 2.77746163813215, 3.2874952059661293, 3.6804820674435823, 3.9832821869498707, 4.216591422853343, 4.396356053214123, 4.534862675988926, 4.641577976503701, 4.723795758832229, 4.7871354645428115, 4.835926251697274, 4.873502885229927, 4.902433662296076, 4.924695950888916, 4.9418113394821415, 4.954949634939837, 4.965008816768869, 4.972676412447021, 4.978476488723142, 4.982805470662491, 4.9859592366063445, 4.988153340938925, 4.9895377468524105, 4.9902070760687325, 2.1155214619699456, 2.777461638132166, 3.287495205966074, 3.6804820674436494, 3.9832821869498685, 4.216591422853293, 4.396356053214151, 4.534862675988926, 4.641577976503699, 4.723795758832234, 4.787135464542815, 4.835926251697278, 4.87350288522993, 4.902433662296076, 4.924695950888913, 4.941811339482138, 4.954949634939832, 4.9650088167688695, 4.972676412447021, 4.978476488723141, 4.982805470662492, 4.985959236606346, 4.988153340938926, 4.989537746852409, 4.990207076068729, 2.115521461969962, 2.777461638132113, 3.2874952059661533, 3.6804820674435756, 3.983282186949894, 4.21659142285333, 4.3963560532140935, 4.534862675988948, 4.641577976503708, 4.723795758832238, 4.787135464542824, 4.835926251697284, 4.873502885229934, 4.902433662296074, 4.924695950888906, 4.941811339482129, 4.954949634939827, 4.965008816768864, 4.9726764124470195, 4.9784764887231425, 4.982805470662496, 4.98595923660635, 4.988153340938925, 4.989537746852403, 4.990207076068724, 2.1155214619699336, 2.777461638132193, 3.2874952059660827, 3.6804820674436236, 3.9832821869498463, 4.21659142285334, 4.396356053214133, 4.534862675988895, 4.641577976503733, 4.72379575883225, 4.787135464542832, 4.835926251697296, 4.873502885229939, 4.9024336622960725, 4.924695950888901, 4.94181133948212, 4.954949634939815, 4.9650088167688535, 4.972676412447014, 4.97847648872314, 4.9828054706624965, 4.985959236606352, 4.988153340938927, 4.9895377468524025, 4.990207076068718, 2.1155214619699465, 2.7774616381321464, 3.287495205966141, 3.680482067443583, 3.983282186949881, 4.216591422853283, 4.396356053214144, 4.534862675988945, 4.641577976503681, 4.723795758832279, 4.787135464542853, 4.835926251697308, 4.873502885229949, 4.902433662296076, 4.924695950888897, 4.9418113394821095, 4.9549496349398, 4.965008816768842, 4.972676412447004, 4.978476488723136, 4.982805470662497, 4.985959236606355, 4.988153340938934, 4.989537746852406, 4.990207076068718, 2.115521461969965, 2.7774616381321353, 3.2874952059661307, 3.6804820674436347, 3.983282186949838, 4.216591422853322, 4.3963560532140775, 4.534862675988952, 4.641577976503745, 4.723795758832235, 4.787135464542882, 4.835926251697332, 4.873502885229963, 4.902433662296084, 4.9246959508888954, 4.941811339482098, 4.954949634939785, 4.965008816768823, 4.972676412446988, 4.978476488723127, 4.982805470662496, 4.985959236606362, 4.988153340938939, 4.989537746852414, 4.990207076068727, 2.1155214619699616, 2.7774616381321873, 3.287495205966097, 3.680482067443629, 3.9832821869499013, 4.216591422853279, 4.39635605321412, 4.534862675988878, 4.641577976503744, 4.723795758832312, 4.787135464542844, 4.835926251697361, 4.873502885229992, 4.902433662296099, 4.9246959508889, 4.94181133948209, 4.9549496349397675, 4.965008816768801, 4.972676412446969, 4.978476488723113, 4.98280547066249, 4.985959236606364, 4.9881533409389505, 4.989537746852428, 4.990207076068748, 2.115521461969961, 2.777461638132167, 3.2874952059661524, 3.6804820674435925, 3.9832821869499035, 4.2165914228533525, 4.396356053214075, 4.5348626759889195, 4.641577976503658, 4.723795758832302, 4.787135464542938, 4.83592625169734, 4.8735028852300255, 4.902433662296131, 4.924695950888914, 4.941811339482091, 4.954949634939754, 4.965008816768776, 4.972676412446941, 4.978476488723093, 4.982805470662478, 4.985959236606366, 4.988153340938966, 4.989537746852457, 4.990207076068792, 2.1155214619699585, 2.7774616381321655, 3.287495205966137, 3.6804820674436463, 3.983282186949857, 4.216591422853364, 4.396356053214162, 4.534862675988877, 4.641577976503705, 4.723795758832208, 4.787135464542919, 4.83592625169745, 4.873502885230019, 4.90243366229617, 4.92469595088895, 4.941811339482107, 4.954949634939747, 4.965008816768752, 4.972676412446909, 4.978476488723062, 4.982805470662458, 4.985959236606364, 4.988153340938987, 4.989537746852505, 4.990207076068866, 2.115521461969955, 2.777461638132161, 3.287495205966126, 3.68048206744363, 3.9832821869499093, 4.216591422853312, 4.396356053214188, 4.53486267598898, 4.6415779765036635, 4.723795758832261, 4.787135464542813, 4.835926251697418, 4.873502885230147, 4.902433662296186, 4.924695950888996, 4.94181133948214, 4.954949634939753, 4.965008816768735, 4.972676412446874, 4.978476488723021, 4.982805470662428, 4.985959236606355, 4.98815334093901, 4.989537746852569, 4.990207076068971, 2.1155214619699465, 2.7774616381321517, 3.2874952059661178, 3.6804820674436143, 3.983282186949893, 4.21659142285336, 4.396356053214128, 4.53486267598902, 4.641577976503782, 4.723795758832218, 4.78713546454288, 4.835926251697309, 4.873502885230105, 4.902433662296334, 4.924695950889035, 4.94181133948219, 4.954949634939786, 4.9650088167687345, 4.972676412446843, 4.978476488722976, 4.982805470662388, 4.985959236606341, 4.988153340939038, 4.989537746852649, 4.9902070760691135, 2.1155214619699425, 2.7774616381321406, 3.287495205966106, 3.680482067443601, 3.9832821869498716, 4.216591422853341, 4.3963560532141654, 4.534862675988948, 4.6415779765038385, 4.723795758832351, 4.787135464542834, 4.835926251697391, 4.87350288523, 4.90243366229628, 4.924695950889204, 4.941811339482259, 4.954949634939842, 4.965008816768761, 4.972676412446831, 4.9784764887229365, 4.9828054706623455, 4.985959236606322, 4.988153340939068, 4.989537746852747, 4.990207076069285, 2.115521461969938, 2.7774616381321353, 3.2874952059660925, 3.680482067443586, 3.983282186949854, 4.216591422853312, 4.396356053214142, 4.5348626759889745, 4.641577976503753, 4.723795758832422, 4.787135464542972, 4.835926251697342, 4.87350288523011, 4.9024336622961915, 4.924695950889147, 4.941811339482447, 4.954949634939936, 4.965008816768823, 4.97267641244685, 4.978476488722916, 4.982805470662308, 4.9859592366063, 4.988153340939096, 4.989537746852852, 4.990207076069479, 2.115521461969938, 2.7774616381321326, 3.2874952059660885, 3.6804820674435716, 3.983282186949836, 4.2165914228532895, 4.396356053214106, 4.534862675988942, 4.641577976503759, 4.723795758832318, 4.7871354645430575, 4.83592625169748, 4.873502885230049, 4.902433662296341, 4.924695950889094, 4.941811339482397, 4.95494963494015, 4.965008816768947, 4.972676412446921, 4.978476488722933, 4.98280547066229, 4.985959236606281, 4.98815334093912, 4.989537746852953, 4.990207076069677, 2.1155214619699416, 2.7774616381321358, 3.2874952059660885, 3.680482067443571, 3.9832821869498236, 4.216591422853272, 4.396356053214076, 4.534862675988894, 4.6415779765037115, 4.723795758832293, 4.787135464542929, 4.835926251697569, 4.87350288523017, 4.902433662296263, 4.924695950889303, 4.941811339482415, 4.954949634940126, 4.965008816769193, 4.972676412447082, 4.978476488723019, 4.9828054706623135, 4.985959236606278, 4.988153340939131, 4.989537746853027, 4.9902070760698365, 2.1155214619699456, 2.7774616381321438, 3.2874952059660965, 3.680482067443577, 3.9832821869498267, 4.21659142285326, 4.396356053214055, 4.534862675988856, 4.641577976503651, 4.723795758832229, 4.787135464542869, 4.83592625169741, 4.8735028852302555, 4.902433662296349, 4.9246959508892, 4.941811339482711, 4.954949634940262, 4.96500881676923, 4.972676412447377, 4.978476488723223, 4.982805470662418, 4.985959236606305, 4.988153340939135, 4.989537746853045, 4.9902070760699075, 2.1155214619699527, 2.7774616381321526, 3.2874952059661084, 3.6804820674435894, 3.983282186949837, 4.216591422853266, 4.396356053214046, 4.534862675988836, 4.641577976503607, 4.723795758832156, 4.787135464542783, 4.835926251697306, 4.873502885230058, 4.902433662296415, 4.924695950889225, 4.941811339482574, 4.954949634940682, 4.965008816769538, 4.972676412447512, 4.9784764887235715, 4.982805470662651, 4.9859592366064, 4.988153340939122, 4.989537746852983, 4.990207076069819, 2.115521461969957, 2.7774616381321615, 3.28749520596612, 3.6804820674436036, 3.983282186949852, 4.2165914228532815, 4.396356053214059, 4.534862675988832, 4.641577976503589, 4.723795758832109, 4.787135464542699, 4.835926251697201, 4.8735028852299145, 4.902433662296182, 4.9246959508892605, 4.941811339482512, 4.954949634940508, 4.9650088167701325, 4.972676412448062, 4.9784764887238415, 4.98280547066304, 4.985959236606607, 4.988153340939116, 4.989537746852791, 4.990207076069488, 2.115521461969959, 2.777461638132165, 3.2874952059661293, 3.6804820674436165, 3.9832821869498702, 4.2165914228533, 4.3963560532140775, 4.53486267598885, 4.6415779765035925, 4.723795758832099, 4.787135464542659, 4.83592625169712, 4.873502885229795, 4.902433662296005, 4.9246959508889985, 4.941811339482505, 4.954949634940328, 4.9650088167699105, 4.972676412448865, 4.978476488724687, 4.982805470663438, 4.985959236606952, 4.988153340939141, 4.989537746852459, 4.990207076068828, 2.115521461969959, 2.7774616381321673, 3.287495205966133, 3.6804820674436236, 3.9832821869498813, 4.216591422853317, 4.396356053214099, 4.534862675988874, 4.641577976503622, 4.723795758832121, 4.787135464542672, 4.8359262516971, 4.873502885229737, 4.902433662295897, 4.92469595088881, 4.94181133948223, 4.954949634940263, 4.965008816769564, 4.972676412448564, 4.9784764887257005, 4.982805470664563, 4.9859592366073775, 4.9881533409392205, 4.989537746851977, 4.990207076067756, 2.1155214619699563, 2.7774616381321633, 3.287495205966129, 3.6804820674436227, 3.9832821869498836, 4.216591422853322, 4.396356053214114, 4.534862675988901, 4.641577976503661, 4.723795758832171, 4.7871354645427235, 4.835926251697157, 4.8735028852297715, 4.902433662295896, 4.9246959508887524, 4.941811339482067, 4.9549496349399895, 4.965008816769406, 4.972676412447958, 4.9784764887252075, 4.9828054706656815, 4.985959236608623, 4.988153340939394, 4.989537746851361, 4.990207076066229, 2.1155214619699514, 2.777461638132155, 3.28749520596612, 3.680482067443612, 3.9832821869498733, 4.216591422853318, 4.3963560532141175, 4.534862675988919, 4.641577976503696, 4.723795758832233, 4.787135464542814, 4.835926251697265, 4.873502885229904, 4.902433662296027, 4.9246959508888555, 4.941811339482099, 4.95494963493988, 4.96500881676912, 4.972676412447615, 4.978476488724162, 4.982805470664763, 4.985959236609568, 4.988153340940375, 4.989537746850758, 4.99020707606428, 2.115521461969946, 2.7774616381321473, 3.287495205966106, 3.6804820674435925, 3.9832821869498507, 4.216591422853299, 4.396356053214109, 4.534862675988926, 4.641577976503724, 4.723795758832294, 4.787135464542917, 4.835926251697422, 4.873502885230109, 4.902433662296279, 4.924695950889122, 4.941811339482341, 4.954949634940019, 4.96500881676904, 4.97267641244722, 4.978476488723418, 4.9828054706629485, 4.985959236607795, 4.988153340940623, 4.9895377468508535, 4.990207076062149, 2.115521461969941, 2.7774616381321344, 3.287495205966085, 3.680482067443565, 3.9832821869498223, 4.216591422853273, 4.396356053214089, 4.5348626759889195, 4.641577976503747, 4.723795758832354, 4.787135464543032, 4.835926251697607, 4.873502885230372, 4.902433662296615, 4.924695950889526, 4.941811339482757, 4.954949634940379, 4.96500881676922, 4.972676412447033, 4.978476488722675, 4.982805470661423, 4.985959236604697, 4.988153340937385, 4.989537746849712, 4.990207076060558, 2.115521461969936, 2.7774616381321215, 3.287495205966064, 3.68048206744354, 3.9832821869497947, 4.216591422853245, 4.396356053214069, 4.534862675988914, 4.641577976503769, 4.723795758832419, 4.787135464543158, 4.83592625169781, 4.873502885230665, 4.902433662297009, 4.92469595089, 4.941811339483287, 4.954949634940883, 4.965008816769582, 4.972676412447073, 4.97847648872212, 4.982805470659965, 4.985959236601895, 4.988153340932358, 4.989537746844231, 4.990207076057311]]]

        phi_test = np.array(phi_test)

        # Test the scalar flux
        l = 0
        phi = pydgm.state.mg_phi[l, :, :].flatten()
        phi_zero_test = phi_test[:, l].flatten()
        np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()

    def test_solver_basic_2D_2g_1a_vacuum(self):
        '''
        Test for a basic 2 group problem
        '''
        self.set_mesh('simple')
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 0.0
        pydgm.control.boundary_south = 0.0
        pydgm.control.allow_fission = False

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[2.1137582766948073, 2.636581917488039, 3.026045587155106, 3.371616718556787, 3.6667806259373976, 3.918852544828727, 4.129290293281016, 4.301839388015012, 4.43913453975634, 4.543496011917352, 4.616741622074667, 4.660168812348085, 4.674557938961098, 4.660168812348085, 4.616741622074666, 4.543496011917352, 4.439134539756339, 4.301839388015011, 4.129290293281011, 3.918852544828722, 3.666780625937393, 3.3716167185567794, 3.0260455871551, 2.6365819174880345, 2.1137582766948024, 2.636581917488038, 3.4335823665029626, 3.9865333116002404, 4.413365681101105, 4.7889411365991865, 5.104453801345153, 5.36923080244542, 5.585594884403345, 5.7577177607817, 5.8884937048816415, 5.980248025842213, 6.034641916141866, 6.052663312839643, 6.034641916141865, 5.980248025842214, 5.888493704881639, 5.757717760781698, 5.585594884403341, 5.369230802445415, 5.104453801345149, 4.78894113659918, 4.413365681101101, 3.986533311600236, 3.433582366502959, 2.636581917488036, 3.0260455871551004, 3.986533311600237, 4.764985911789622, 5.3195594392634815, 5.755716685290208, 6.1360848502194845, 6.449966786612971, 6.708038228026866, 6.912828986796572, 7.068443611677266, 7.177617595002775, 7.242328637658107, 7.263768519691014, 7.242328637658108, 7.177617595002773, 7.068443611677264, 6.912828986796565, 6.708038228026858, 6.449966786612963, 6.136084850219477, 5.755716685290201, 5.319559439263479, 4.764985911789622, 3.9865333116002364, 3.026045587155101, 3.3716167185567794, 4.413365681101101, 5.319559439263478, 6.059734933640805, 6.594669919226913, 7.019009405830075, 7.385013603583526, 7.680284321463562, 7.916262866710092, 8.095197815005834, 8.220753908477315, 8.295185933912736, 8.319842223627575, 8.295185933912736, 8.220753908477313, 8.095197815005829, 7.9162628667100865, 7.680284321463553, 7.385013603583518, 7.019009405830066, 6.5946699192269085, 6.0597349336408035, 5.319559439263479, 4.413365681101103, 3.3716167185567816, 3.666780625937396, 4.788941136599183, 5.755716685290202, 6.594669919226909, 7.282837454229495, 7.7826243439997524, 8.17920924579081, 8.516051572939901, 8.77921200419981, 8.980435993926783, 9.1213414136694, 9.204876783614267, 9.232563239373745, 9.20487678361426, 9.121341413669393, 8.980435993926774, 8.779212004199799, 8.516051572939887, 8.179209245790801, 7.782624343999744, 7.28283745422949, 6.594669919226911, 5.755716685290203, 4.788941136599184, 3.6667806259373954, 3.918852544828727, 5.104453801345156, 6.136084850219482, 7.019009405830074, 7.7826243439997524, 8.40938822057789, 8.862542988092518, 9.219039481903943, 9.514904344894836, 9.734791360013814, 9.890382762980401, 9.982413174745984, 10.012890843410913, 9.982413174745975, 9.890382762980387, 9.734791360013801, 9.514904344894822, 9.219039481903929, 8.862542988092505, 8.40938822057788, 7.782624343999746, 7.019009405830071, 6.136084850219481, 5.104453801345154, 3.918852544828727, 4.129290293281017, 5.369230802445423, 6.449966786612975, 7.385013603583529, 8.179209245790814, 8.86254298809252, 9.421325551938462, 9.819043013362487, 10.125544719186678, 10.370617986609494, 10.537607630974078, 10.637814624227977, 10.67092412242758, 10.637814624227971, 10.537607630974074, 10.37061798660948, 10.125544719186667, 9.81904301336248, 9.421325551938448, 8.862542988092509, 8.179209245790803, 7.385013603583525, 6.449966786612973, 5.369230802445423, 4.129290293281019, 4.301839388015017, 5.585594884403349, 6.70803822802687, 7.680284321463569, 8.516051572939904, 9.219039481903947, 9.819043013362498, 10.305028855809763, 10.640260599269606, 10.888489126670626, 11.074282265530496, 11.179757933772853, 11.215539376713828, 11.179757933772844, 11.074282265530494, 10.888489126670617, 10.640260599269597, 10.305028855809747, 9.819043013362476, 9.219039481903932, 8.516051572939894, 7.680284321463562, 6.708038228026868, 5.585594884403352, 4.301839388015019, 4.439134539756346, 5.7577177607817065, 6.912828986796578, 7.916262866710104, 8.779212004199813, 9.51490434489484, 10.125544719186685, 10.64026059926961, 11.049730149466411, 11.31657882466728, 11.499364812828357, 11.618289856582024, 11.653913937623651, 11.61828985658202, 11.499364812828354, 11.316578824667275, 11.049730149466402, 10.640260599269599, 10.12554471918667, 9.514904344894827, 8.779212004199808, 7.916262866710098, 6.912828986796577, 5.757717760781709, 4.439134539756347, 4.543496011917359, 5.888493704881649, 7.068443611677271, 8.095197815005841, 8.98043599392679, 9.734791360013816, 10.370617986609494, 10.88848912667063, 11.316578824667287, 11.64652310519862, 11.839888723085174, 11.950458326084561, 11.997247515430729, 11.950458326084556, 11.839888723085167, 11.646523105198613, 11.316578824667275, 10.888489126670617, 10.370617986609481, 9.734791360013805, 8.980435993926779, 8.095197815005836, 7.068443611677272, 5.888493704881652, 4.543496011917362, 4.61674162207467, 5.980248025842219, 7.177617595002779, 8.22075390847732, 9.121341413669404, 9.890382762980396, 10.537607630974078, 11.074282265530497, 11.499364812828357, 11.839888723085176, 12.08742129738902, 12.20452583801236, 12.231939627403282, 12.204525838012362, 12.087421297389014, 11.839888723085165, 11.499364812828354, 11.074282265530488, 10.537607630974072, 9.890382762980394, 9.121341413669398, 8.220753908477317, 7.177617595002782, 5.980248025842224, 4.6167416220746755, 4.660168812348088, 6.03464191614187, 7.242328637658109, 8.295185933912737, 9.204876783614266, 9.982413174745979, 10.637814624227977, 11.17975793377285, 11.61828985658203, 11.95045832608456, 12.20452583801236, 12.36242521569222, 12.403495350196929, 12.36242521569222, 12.204525838012351, 11.950458326084558, 11.618289856582022, 11.179757933772846, 10.637814624227973, 9.982413174745977, 9.20487678361426, 8.295185933912736, 7.2423286376581135, 6.034641916141876, 4.660168812348094, 4.674557938961099, 6.052663312839645, 7.263768519691019, 8.319842223627575, 9.232563239373746, 10.012890843410915, 10.67092412242758, 11.215539376713833, 11.653913937623651, 11.99724751543073, 12.231939627403282, 12.403495350196932, 12.490278681424238, 12.403495350196927, 12.231939627403277, 11.997247515430733, 11.653913937623647, 11.215539376713828, 10.670924122427579, 10.012890843410915, 9.232563239373748, 8.31984222362758, 7.263768519691021, 6.05266331283965, 4.674557938961106, 4.660168812348089, 6.034641916141869, 7.24232863765811, 8.295185933912737, 9.204876783614264, 9.98241317474598, 10.63781462422798, 11.179757933772853, 11.61828985658203, 11.950458326084561, 12.204525838012364, 12.362425215692218, 12.40349535019693, 12.362425215692218, 12.204525838012357, 11.950458326084558, 11.618289856582027, 11.179757933772848, 10.637814624227977, 9.982413174745984, 9.204876783614267, 8.29518593391274, 7.2423286376581135, 6.034641916141875, 4.660168812348094, 4.616741622074671, 5.980248025842217, 7.177617595002775, 8.220753908477317, 9.121341413669398, 9.890382762980392, 10.537607630974076, 11.0742822655305, 11.499364812828361, 11.839888723085176, 12.087421297389016, 12.204525838012358, 12.231939627403277, 12.204525838012355, 12.087421297389016, 11.839888723085169, 11.499364812828361, 11.074282265530499, 10.537607630974078, 9.890382762980403, 9.121341413669404, 8.220753908477318, 7.177617595002784, 5.980248025842225, 4.616741622074678, 4.5434960119173535, 5.888493704881644, 7.068443611677267, 8.095197815005829, 8.980435993926775, 9.734791360013807, 10.370617986609489, 10.888489126670626, 11.316578824667278, 11.646523105198616, 11.839888723085169, 11.95045832608456, 11.99724751543073, 11.950458326084556, 11.83988872308517, 11.646523105198614, 11.31657882466728, 10.888489126670631, 10.370617986609496, 9.73479136001382, 8.980435993926786, 8.095197815005838, 7.068443611677275, 5.888493704881654, 4.543496011917363, 4.4391345397563375, 5.7577177607816985, 6.912828986796568, 7.916262866710087, 8.779212004199803, 9.514904344894827, 10.125544719186676, 10.640260599269608, 11.049730149466406, 11.316578824667276, 11.499364812828356, 11.61828985658202, 11.653913937623644, 11.618289856582027, 11.499364812828356, 11.316578824667276, 11.049730149466411, 10.640260599269613, 10.125544719186681, 9.51490434489484, 8.779212004199811, 7.916262866710099, 6.912828986796576, 5.757717760781707, 4.439134539756347, 4.301839388015011, 5.58559488440334, 6.708038228026859, 7.680284321463556, 8.51605157293989, 9.219039481903934, 9.819043013362487, 10.305028855809757, 10.640260599269604, 10.88848912667062, 11.074282265530497, 11.179757933772846, 11.215539376713828, 11.179757933772846, 11.074282265530496, 10.888489126670626, 10.640260599269608, 10.30502885580976, 9.819043013362489, 9.219039481903943, 8.516051572939903, 7.680284321463565, 6.708038228026868, 5.585594884403352, 4.3018393880150185, 4.12929029328101, 5.369230802445414, 6.449966786612966, 7.3850136035835225, 8.179209245790803, 8.862542988092512, 9.42132555193845, 9.819043013362489, 10.125544719186678, 10.37061798660949, 10.537607630974074, 10.637814624227977, 10.670924122427584, 10.637814624227978, 10.537607630974083, 10.370617986609492, 10.125544719186678, 9.81904301336249, 9.421325551938459, 8.862542988092521, 8.17920924579081, 7.38501360358353, 6.4499667866129755, 5.369230802445425, 4.129290293281018, 3.91885254482872, 5.104453801345149, 6.136084850219476, 7.019009405830068, 7.782624343999747, 8.409388220577886, 8.86254298809251, 9.21903948190394, 9.514904344894834, 9.734791360013814, 9.890382762980398, 9.982413174745982, 10.012890843410915, 9.982413174745984, 9.890382762980401, 9.734791360013817, 9.514904344894838, 9.219039481903938, 8.862542988092521, 8.409388220577892, 7.782624343999754, 7.019009405830075, 6.136084850219486, 5.104453801345158, 3.918852544828728, 3.6667806259373914, 4.78894113659918, 5.755716685290201, 6.594669919226909, 7.28283745422949, 7.782624343999746, 8.179209245790807, 8.5160515729399, 8.77921200419981, 8.980435993926783, 9.121341413669407, 9.204876783614267, 9.23256323937375, 9.204876783614273, 9.121341413669406, 8.980435993926788, 8.77921200419981, 8.5160515729399, 8.179209245790808, 7.7826243439997524, 7.282837454229498, 6.594669919226916, 5.755716685290205, 4.788941136599187, 3.6667806259373967, 3.37161671855678, 4.413365681101101, 5.319559439263477, 6.059734933640802, 6.5946699192269085, 7.0190094058300705, 7.385013603583527, 7.680284321463568, 7.916262866710099, 8.09519781500584, 8.220753908477324, 8.295185933912745, 8.319842223627582, 8.295185933912743, 8.220753908477322, 8.095197815005838, 7.916262866710101, 7.680284321463565, 7.385013603583527, 7.019009405830073, 6.5946699192269165, 6.059734933640807, 5.319559439263479, 4.413365681101102, 3.371616718556781, 3.026045587155099, 3.9865333116002355, 4.764985911789621, 5.319559439263474, 5.755716685290202, 6.136084850219482, 6.449966786612975, 6.708038228026869, 6.912828986796578, 7.068443611677276, 7.177617595002782, 7.242328637658115, 7.263768519691024, 7.242328637658114, 7.177617595002782, 7.068443611677276, 6.91282898679658, 6.708038228026866, 6.449966786612972, 6.136084850219481, 5.755716685290203, 5.319559439263478, 4.764985911789619, 3.9865333116002333, 3.0260455871550973, 2.6365819174880283, 3.433582366502954, 3.986533311600234, 4.413365681101106, 4.788941136599191, 5.104453801345162, 5.369230802445426, 5.585594884403354, 5.757717760781711, 5.888493704881652, 5.980248025842221, 6.034641916141872, 6.052663312839648, 6.034641916141873, 5.980248025842222, 5.88849370488165, 5.757717760781708, 5.58559488440335, 5.369230802445423, 5.104453801345157, 4.788941136599186, 4.4133656811011015, 3.986533311600232, 3.4335823665029483, 2.636581917488022, 2.113758276694795, 2.636581917488029, 3.0260455871551013, 3.3716167185567865, 3.666780625937402, 3.9188525448287326, 4.129290293281024, 4.30183938801502, 4.439134539756346, 4.543496011917359, 4.616741622074675, 4.6601688123480915, 4.674557938961102, 4.66016881234809, 4.616741622074674, 4.54349601191736, 4.4391345397563455, 4.301839388015018, 4.129290293281022, 3.91885254482873, 3.6667806259373985, 3.371616718556779, 3.0260455871550938, 2.6365819174880216, 2.11375827669479]], [[1.4767264367289454, 2.0536115658036045, 2.4501895371664633, 2.769756152635721, 3.0178250504254187, 3.2116431023155574, 3.360859644160609, 3.475513976480186, 3.5616249895027488, 3.6242461228006966, 3.666736503780116, 3.6913689043365716, 3.699440712242182, 3.6913689043365707, 3.666736503780114, 3.624246122800694, 3.561624989502746, 3.475513976480182, 3.3608596441606076, 3.211643102315556, 3.0178250504254156, 2.7697561526357193, 2.450189537166463, 2.0536115658036023, 1.476726436728944, 2.053611565803603, 2.9806508783667836, 3.594949481069355, 4.041192377459999, 4.399655593175661, 4.676062267018393, 4.891427824136701, 5.056008833791333, 5.18036209966473, 5.270748798231736, 5.332176789846988, 5.367815445130931, 5.379493675422171, 5.367815445130932, 5.3321767898469865, 5.2707487982317325, 5.180362099664724, 5.056008833791329, 4.891427824136698, 4.676062267018389, 4.399655593175656, 4.041192377459995, 3.5949494810693516, 2.9806508783667813, 2.053611565803603, 2.450189537166463, 3.594949481069355, 4.45557153192178, 5.048969549536415, 5.494034596665513, 5.85133278235618, 6.125118539119001, 6.337114918558057, 6.496329623276333, 6.612650566613521, 6.691642932786554, 6.737508894986761, 6.752551290663871, 6.737508894986762, 6.691642932786551, 6.6126505666135165, 6.496329623276329, 6.337114918558051, 6.125118539118993, 5.851332782356174, 5.494034596665506, 5.04896954953641, 4.455571531921775, 3.594949481069352, 2.4501895371664615, 2.769756152635722, 4.041192377459998, 5.048969549536414, 5.81893429279327, 6.364366237392115, 6.781718477169064, 7.115632644688468, 7.3685696691782505, 7.561517028803791, 7.701421995516999, 7.796908865110687, 7.85229656349987, 7.870455566936735, 7.852296563499866, 7.796908865110681, 7.701421995516996, 7.561517028803788, 7.368569669178243, 7.11563264468846, 6.781718477169059, 6.364366237392108, 5.818934292793264, 5.048969549536411, 4.041192377459995, 2.7697561526357193, 3.0178250504254174, 4.399655593175659, 5.49403459666551, 6.364366237392114, 7.038462665587848, 7.523991240371386, 7.899375123783939, 8.19699542212261, 8.41762546391737, 8.580784108132265, 8.69101588151382, 8.755320614100603, 8.776386094007659, 8.755320614100603, 8.691015881513819, 8.58078410813226, 8.417625463917357, 8.196995422122601, 7.8993751237839325, 7.523991240371379, 7.038462665587842, 6.364366237392106, 5.4940345966655055, 4.399655593175656, 3.017825050425416, 3.2116431023155574, 4.6760622670183905, 5.85133278235618, 6.781718477169063, 7.5239912403713864, 8.104277290662166, 8.525040454068225, 8.850655152516179, 9.104145446405983, 9.28471412881898, 9.409988549808515, 9.481974487228463, 9.505771074606805, 9.481974487228467, 9.409988549808512, 9.284714128818969, 9.10414544640597, 8.850655152516165, 8.525040454068211, 8.104277290662157, 7.523991240371374, 6.781718477169058, 5.851332782356172, 4.676062267018387, 3.2116431023155547, 3.360859644160608, 4.891427824136697, 6.125118539118997, 7.115632644688469, 7.899375123783939, 8.525040454068227, 9.016095450707015, 9.370641412825156, 9.642142018518644, 9.846394441040012, 9.981067128226861, 10.061616277791211, 10.087320592479987, 10.061616277791208, 9.981067128226854, 9.846394441040006, 9.64214201851863, 9.37064141282514, 9.016095450707004, 8.525040454068215, 7.899375123783932, 7.11563264468846, 6.125118539118992, 4.891427824136693, 3.3608596441606036, 3.4755139764801837, 5.056008833791331, 6.337114918558055, 7.36856966917825, 8.196995422122612, 8.850655152516179, 9.370641412825155, 9.777620689458715, 10.066035229392874, 10.28081219824272, 10.432034289079153, 10.515655792353899, 10.545275368624662, 10.515655792353899, 10.432034289079148, 10.280812198242712, 10.066035229392858, 9.777620689458702, 9.37064141282514, 8.850655152516167, 8.196995422122601, 7.368569669178241, 6.337114918558049, 5.056008833791327, 3.4755139764801806, 3.5616249895027474, 5.180362099664729, 6.496329623276332, 7.561517028803792, 8.41762546391737, 9.104145446405981, 9.642142018518644, 10.06603522939287, 10.393790492194215, 10.616656169989959, 10.772672174346603, 10.867813795448603, 10.894360150480162, 10.867813795448603, 10.772672174346596, 10.616656169989948, 10.3937904921942, 10.066035229392854, 9.64214201851863, 9.104145446405969, 8.41762546391736, 7.561517028803784, 6.496329623276324, 5.180362099664722, 3.5616249895027434, 3.6242461228006966, 5.270748798231736, 6.612650566613521, 7.701421995517, 8.580784108132269, 9.284714128818985, 9.846394441040017, 10.280812198242721, 10.616656169989957, 10.869209298799491, 11.027337059982218, 11.121638960398776, 11.158788722839008, 11.121638960398776, 11.02733705998221, 10.869209298799477, 10.616656169989946, 10.280812198242707, 9.846394441040001, 9.284714128818967, 8.580784108132256, 7.701421995516991, 6.612650566613514, 5.270748798231729, 3.6242461228006935, 3.666736503780114, 5.332176789846987, 6.6916429327865545, 7.796908865110688, 8.69101588151383, 9.409988549808519, 9.981067128226861, 10.432034289079157, 10.772672174346605, 11.02733705998222, 11.20686735617178, 11.30192763378054, 11.331229666432739, 11.301927633780531, 11.20686735617177, 11.027337059982205, 10.772672174346594, 10.432034289079148, 9.981067128226854, 9.409988549808507, 8.691015881513815, 7.796908865110677, 6.691642932786546, 5.332176789846984, 3.6667365037801107, 3.69136890433657, 5.367815445130929, 6.737508894986762, 7.852296563499869, 8.755320614100611, 9.481974487228475, 10.06161627779122, 10.515655792353908, 10.867813795448614, 11.12163896039878, 11.301927633780542, 11.409796082720524, 11.436653246156595, 11.409796082720513, 11.30192763378053, 11.12163896039877, 10.8678137954486, 10.515655792353895, 10.06161627779121, 9.481974487228463, 8.755320614100597, 7.852296563499859, 6.737508894986757, 5.367815445130929, 3.6913689043365685, 3.6994407122421826, 5.3794936754221725, 6.752551290663872, 7.870455566936736, 8.776386094007666, 9.505771074606814, 10.087320592479994, 10.545275368624665, 10.894360150480173, 11.158788722839018, 11.331229666432744, 11.436653246156599, 11.485906230578191, 11.436653246156594, 11.33122966643273, 11.158788722839, 10.89436015048016, 10.545275368624655, 10.087320592479983, 9.505771074606805, 8.776386094007654, 7.870455566936726, 6.752551290663868, 5.379493675422171, 3.6994407122421813, 3.691368904336571, 5.367815445130932, 6.737508894986764, 7.852296563499871, 8.75532061410061, 9.481974487228472, 10.061616277791215, 10.515655792353906, 10.867813795448614, 11.121638960398782, 11.301927633780544, 11.409796082720526, 11.436653246156595, 11.40979608272052, 11.301927633780533, 11.121638960398773, 10.867813795448596, 10.515655792353893, 10.06161627779121, 9.481974487228465, 8.7553206141006, 7.852296563499864, 6.73750889498676, 5.3678154451309315, 3.6913689043365703, 3.6667365037801134, 5.332176789846987, 6.6916429327865545, 7.79690886511069, 8.691015881513826, 9.409988549808523, 9.981067128226861, 10.432034289079157, 10.772672174346612, 11.027337059982218, 11.206867356171783, 11.301927633780545, 11.33122966643274, 11.301927633780535, 11.206867356171777, 11.02733705998221, 10.772672174346594, 10.432034289079148, 9.981067128226849, 9.409988549808507, 8.691015881513819, 7.796908865110685, 6.691642932786552, 5.332176789846987, 3.6667365037801125, 3.6242461228006957, 5.270748798231736, 6.612650566613523, 7.701421995517, 8.580784108132269, 9.284714128818983, 9.846394441040015, 10.280812198242723, 10.616656169989962, 10.869209298799493, 11.027337059982218, 11.121638960398778, 11.158788722839013, 11.121638960398782, 11.027337059982216, 10.869209298799483, 10.61665616998995, 10.280812198242712, 9.846394441040005, 9.284714128818973, 8.58078410813226, 7.701421995516997, 6.612650566613518, 5.270748798231733, 3.624246122800695, 3.561624989502747, 5.1803620996647295, 6.496329623276332, 7.561517028803793, 8.417625463917368, 9.104145446405983, 9.642142018518644, 10.06603522939287, 10.393790492194213, 10.616656169989959, 10.772672174346605, 10.867813795448605, 10.894360150480168, 10.86781379544861, 10.772672174346601, 10.616656169989954, 10.393790492194206, 10.06603522939286, 9.642142018518634, 9.104145446405973, 8.41762546391736, 7.561517028803788, 6.496329623276331, 5.1803620996647295, 3.5616249895027474, 3.475513976480184, 5.056008833791331, 6.337114918558059, 7.368569669178249, 8.19699542212261, 8.850655152516179, 9.370641412825155, 9.777620689458713, 10.066035229392867, 10.280812198242717, 10.432034289079153, 10.515655792353906, 10.545275368624662, 10.5156557923539, 10.432034289079152, 10.280812198242712, 10.066035229392861, 9.777620689458704, 9.370641412825144, 8.850655152516172, 8.196995422122603, 7.368569669178246, 6.337114918558055, 5.056008833791332, 3.4755139764801855, 3.3608596441606076, 4.891427824136698, 6.125118539118999, 7.115632644688468, 7.899375123783939, 8.525040454068225, 9.016095450707015, 9.370641412825153, 9.642142018518642, 9.846394441040012, 9.981067128226858, 10.061616277791218, 10.087320592479992, 10.061616277791213, 9.981067128226854, 9.846394441040008, 9.642142018518634, 9.370641412825144, 9.016095450707004, 8.525040454068215, 7.899375123783936, 7.115632644688464, 6.125118539118995, 4.891427824136698, 3.3608596441606085, 3.2116431023155565, 4.6760622670183905, 5.851332782356179, 6.781718477169064, 7.523991240371383, 8.104277290662164, 8.52504045406822, 8.850655152516177, 9.10414544640598, 9.28471412881898, 9.409988549808514, 9.48197448722847, 9.50577107460681, 9.481974487228467, 9.40998854980851, 9.284714128818974, 9.104145446405976, 8.850655152516172, 8.525040454068213, 8.104277290662159, 7.523991240371381, 6.781718477169062, 5.851332782356178, 4.6760622670183905, 3.2116431023155583, 3.0178250504254183, 4.39965559317566, 5.494034596665512, 6.364366237392111, 7.038462665587846, 7.52399124037138, 7.899375123783936, 8.196995422122605, 8.417625463917366, 8.580784108132264, 8.69101588151382, 8.755320614100606, 8.776386094007663, 8.7553206141006, 8.691015881513817, 8.58078410813226, 8.417625463917362, 8.196995422122601, 7.899375123783928, 7.523991240371378, 7.038462665587844, 6.364366237392112, 5.494034596665513, 4.399655593175662, 3.0178250504254196, 2.7697561526357215, 4.041192377460001, 5.048969549536414, 5.818934292793269, 6.364366237392113, 6.781718477169062, 7.115632644688465, 7.368569669178244, 7.561517028803786, 7.701421995516996, 7.796908865110683, 7.852296563499866, 7.87045556693673, 7.8522965634998645, 7.796908865110679, 7.701421995516995, 7.561517028803784, 7.36856966917824, 7.1156326446884615, 6.781718477169056, 6.364366237392108, 5.818934292793268, 5.048969549536415, 4.041192377460001, 2.769756152635721, 2.4501895371664633, 3.5949494810693534, 4.455571531921776, 5.048969549536413, 5.494034596665512, 5.851332782356177, 6.1251185391189935, 6.337114918558053, 6.496329623276328, 6.612650566613516, 6.6916429327865465, 6.737508894986757, 6.752551290663868, 6.7375088949867585, 6.691642932786549, 6.612650566613514, 6.496329623276323, 6.337114918558048, 6.125118539118991, 5.851332782356175, 5.494034596665507, 5.048969549536414, 4.455571531921776, 3.5949494810693525, 2.4501895371664637, 2.053611565803603, 2.9806508783667827, 3.594949481069354, 4.041192377460001, 4.399655593175661, 4.67606226701839, 4.891427824136697, 5.05600883379133, 5.180362099664725, 5.270748798231732, 5.332176789846985, 5.367815445130927, 5.37949367542217, 5.367815445130928, 5.332176789846985, 5.270748798231729, 5.1803620996647215, 5.056008833791325, 4.891427824136693, 4.676062267018388, 4.399655593175656, 4.041192377459996, 3.594949481069352, 2.9806508783667813, 2.0536115658036027, 1.476726436728944, 2.0536115658036027, 2.4501895371664637, 2.769756152635721, 3.0178250504254183, 3.2116431023155556, 3.3608596441606067, 3.4755139764801837, 3.5616249895027456, 3.6242461228006935, 3.666736503780112, 3.691368904336567, 3.6994407122421795, 3.691368904336569, 3.6667365037801116, 3.624246122800693, 3.5616249895027448, 3.47551397648018, 3.3608596441606036, 3.2116431023155547, 3.0178250504254165, 2.7697561526357197, 2.450189537166461, 2.0536115658036027, 1.4767264367289434]]]

        phi_test = np.array(phi_test)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten()
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 7)

        self.angular_test()

    # @unittest.skipIf(anisotropicBroken, 'Anisotropic is not working yet')
    def test_solver_basic_2D_2g_8a_vacuum_l1(self):
        '''
        Test for a basic 2 group problem
        '''
        self.set_mesh('simple')
        pydgm.control.material_map = [2]
        pydgm.control.angle_order = 8
        pydgm.control.boundary_east = 1.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0
        pydgm.control.allow_fission = False
        pydgm.control.scatter_leg_order = 1

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[7.944769557821402, 9.92404624151111, 11.441417546161647, 12.70101298873425, 13.797285229027363, 14.77606964990386, 15.66131416922451, 16.466847477759295, 17.201611655021587, 17.872027197474804, 18.48309040522077, 19.03890345277915, 19.542945487578862, 19.99822182135533, 20.407353085659523, 20.7726329553786, 21.096068141198533, 21.379407542993654, 21.624164250774054, 21.83163250470986, 22.00290090643552, 22.138862717583724, 22.24022380814242, 22.307508641396147, 22.341064561484522, 7.944769557821408, 9.924046241511093, 11.441417546161633, 12.701012988734272, 13.797285229027361, 14.776069649903853, 15.661314169224529, 16.46684747775929, 17.201611655021576, 17.8720271974748, 18.48309040522078, 19.038903452779156, 19.54294548757885, 19.99822182135532, 20.407353085659516, 20.7726329553786, 21.096068141198522, 21.37940754299364, 21.62416425077404, 21.831632504709823, 22.00290090643548, 22.138862717583663, 22.240223808142332, 22.30750864139607, 22.341064561484416, 7.944769557821414, 9.924046241511107, 11.441417546161631, 12.701012988734243, 13.797285229027379, 14.776069649903864, 15.661314169224514, 16.466847477759302, 17.201611655021587, 17.872027197474804, 18.483090405220764, 19.038903452779135, 19.542945487578873, 19.998221821355326, 20.40735308565949, 20.77263295537856, 21.096068141198508, 21.379407542993622, 21.624164250773998, 21.831632504709773, 22.00290090643539, 22.138862717583553, 22.24022380814221, 22.307508641395895, 22.341064561484256, 7.94476955782141, 9.924046241511107, 11.44141754616162, 12.701012988734254, 13.79728522902737, 14.77606964990387, 15.66131416922454, 16.466847477759277, 17.201611655021576, 17.87202719747481, 18.483090405220775, 19.038903452779138, 19.542945487578844, 19.998221821355315, 20.407353085659487, 20.77263295537856, 21.096068141198487, 21.37940754299359, 21.624164250773948, 21.83163250470967, 22.002900906435254, 22.138862717583383, 22.240223808141984, 22.30750864139566, 22.341064561483996, 7.944769557821407, 9.924046241511098, 11.441417546161649, 12.701012988734245, 13.797285229027368, 14.776069649903866, 15.661314169224541, 16.4668474777593, 17.201611655021562, 17.872027197474807, 18.48309040522076, 19.03890345277912, 19.542945487578862, 19.99822182135533, 20.407353085659445, 20.772632955378505, 21.09606814119846, 21.37940754299356, 21.62416425077387, 21.83163250470956, 22.002900906435077, 22.138862717583148, 22.240223808141728, 22.307508641395344, 22.34106456148366, 7.944769557821403, 9.924046241511107, 11.441417546161624, 12.701012988734277, 13.797285229027366, 14.77606964990384, 15.661314169224546, 16.466847477759305, 17.20161165502159, 17.872027197474804, 18.48309040522075, 19.03890345277911, 19.542945487578827, 19.998221821355322, 20.407353085659445, 20.77263295537847, 21.096068141198394, 21.379407542993512, 21.624164250773813, 21.83163250470942, 22.00290090643487, 22.13886271758287, 22.240223808141376, 22.30750864139495, 22.34106456148322, 7.944769557821403, 9.924046241511094, 11.441417546161635, 12.701012988734247, 13.797285229027395, 14.776069649903869, 15.661314169224525, 16.466847477759316, 17.201611655021583, 17.87202719747481, 18.483090405220768, 19.038903452779103, 19.54294548757883, 19.998221821355305, 20.40735308565942, 20.772632955378434, 21.096068141198362, 21.379407542993462, 21.62416425077373, 21.831632504709283, 22.00290090643463, 22.138862717582537, 22.240223808140975, 22.307508641394477, 22.341064561482725, 7.944769557821393, 9.924046241511103, 11.441417546161624, 12.701012988734252, 13.797285229027363, 14.776069649903873, 15.661314169224552, 16.466847477759313, 17.2016116550216, 17.872027197474807, 18.48309040522076, 19.038903452779106, 19.542945487578816, 19.9982218213553, 20.407353085659413, 20.772632955378377, 21.096068141198288, 21.379407542993405, 21.624164250773656, 21.831632504709123, 22.00290090643437, 22.13886271758217, 22.2402238081405, 22.30750864139394, 22.34106456148214, 7.944769557821422, 9.924046241511093, 11.441417546161642, 12.701012988734234, 13.797285229027365, 14.77606964990387, 15.661314169224525, 16.46684747775933, 17.20161165502161, 17.872027197474836, 18.483090405220796, 19.03890345277912, 19.54294548757878, 19.998221821355266, 20.4073530856594, 20.772632955378356, 21.09606814119822, 21.379407542993327, 21.624164250773564, 21.831632504708978, 22.00290090643409, 22.138862717581762, 22.240223808139994, 22.307508641393326, 22.341064561481524, 7.944769557821383, 9.924046241511101, 11.441417546161626, 12.701012988734265, 13.797285229027356, 14.776069649903864, 15.661314169224545, 16.466847477759288, 17.20161165502162, 17.87202719747483, 18.483090405220782, 19.038903452779156, 19.542945487578802, 19.998221821355234, 20.40735308565935, 20.77263295537831, 21.096068141198163, 21.379407542993256, 21.62416425077349, 21.831632504708832, 22.002900906433847, 22.138862717581354, 22.240223808139454, 22.307508641392698, 22.34106456148088, 7.944769557821409, 9.924046241511075, 11.44141754616163, 12.701012988734236, 13.797285229027363, 14.77606964990386, 15.661314169224525, 16.466847477759316, 17.201611655021587, 17.87202719747483, 18.483090405220775, 19.03890345277913, 19.54294548757882, 19.998221821355223, 20.407353085659356, 20.772632955378274, 21.096068141198064, 21.37940754299315, 21.624164250773426, 21.831632504708754, 22.00290090643361, 22.138862717580945, 22.240223808138893, 22.307508641392037, 22.34106456148023, 7.944769557821372, 9.92404624151111, 11.441417546161606, 12.70101298873425, 13.797285229027349, 14.776069649903839, 15.661314169224537, 16.46684747775926, 17.201611655021594, 17.87202719747483, 18.483090405220768, 19.038903452779135, 19.5429454875788, 19.99822182135517, 20.407353085659285, 20.772632955378285, 21.09606814119805, 21.379407542993068, 21.624164250773333, 21.83163250470866, 22.002900906433446, 22.138862717580608, 22.240223808138353, 22.3075086413914, 22.341064561479623, 7.944769557821396, 9.924046241511068, 11.441417546161645, 12.701012988734231, 13.797285229027372, 14.776069649903848, 15.661314169224505, 16.46684747775929, 17.201611655021527, 17.872027197474782, 18.483090405220736, 19.038903452779106, 19.542945487578844, 19.998221821355187, 20.40735308565925, 20.772632955378203, 21.096068141197986, 21.37940754299299, 21.624164250773294, 21.831632504708654, 22.00290090643334, 22.138862717580313, 22.2402238081379, 22.307508641390832, 22.341064561479122, 7.944769557821361, 9.924046241511089, 11.441417546161599, 12.701012988734236, 13.797285229027349, 14.776069649903858, 15.661314169224518, 16.466847477759277, 17.20161165502155, 17.87202719747474, 18.483090405220693, 19.038903452779007, 19.542945487578745, 19.998221821355216, 20.40735308565923, 20.772632955378203, 21.096068141197946, 21.37940754299288, 21.62416425077319, 21.831632504708683, 22.002900906433393, 22.138862717580185, 22.24022380813754, 22.30750864139038, 22.341064561478778, 7.944769557821391, 9.924046241511046, 11.44141754616161, 12.701012988734211, 13.797285229027313, 14.77606964990382, 15.661314169224474, 16.466847477759266, 17.20161165502153, 17.872027197474747, 18.483090405220686, 19.03890345277899, 19.542945487578656, 19.99822182135509, 20.407353085659174, 20.77263295537813, 21.096068141197943, 21.379407542992862, 21.624164250773145, 21.831632504708725, 22.002900906433513, 22.13886271758025, 22.24022380813741, 22.307508641390136, 22.34106456147868, 7.944769557821364, 9.9240462415111, 11.441417546161581, 12.701012988734224, 13.797285229027311, 14.776069649903796, 15.661314169224461, 16.466847477759188, 17.20161165502149, 17.87202719747467, 18.483090405220626, 19.038903452778964, 19.542945487578603, 19.998221821355056, 20.407353085659096, 20.77263295537803, 21.09606814119788, 21.379407542992805, 21.624164250773106, 21.83163250470888, 22.002900906433855, 22.13886271758052, 22.240223808137525, 22.3075086413902, 22.34106456147893, 7.9447695578213615, 9.924046241511041, 11.44141754616162, 12.701012988734218, 13.797285229027331, 14.776069649903809, 15.661314169224468, 16.466847477759188, 17.20161165502142, 17.872027197474623, 18.483090405220494, 19.038903452778836, 19.54294548757849, 19.998221821354907, 20.407353085659047, 20.77263295537799, 21.09606814119789, 21.37940754299286, 21.624164250773052, 21.831632504708917, 22.002900906434302, 22.1388627175812, 22.240223808138055, 22.307508641390637, 22.34106456147965, 7.944769557821303, 9.924046241511027, 11.441417546161542, 12.701012988734183, 13.797285229027299, 14.776069649903793, 15.661314169224445, 16.466847477759185, 17.201611655021427, 17.87202719747459, 18.483090405220448, 19.038903452778744, 19.542945487578347, 19.998221821354726, 20.407353085658844, 20.77263295537782, 21.09606814119778, 21.379407542992954, 21.624164250773223, 21.83163250470914, 22.00290090643485, 22.13886271758208, 22.240223808139046, 22.307508641391657, 22.34106456148094, 7.944769557821265, 9.924046241510942, 11.441417546161507, 12.701012988734096, 13.797285229027194, 14.776069649903686, 15.661314169224324, 16.466847477759075, 17.2016116550213, 17.87202719747451, 18.48309040522039, 19.038903452778673, 19.54294548757834, 19.998221821354665, 20.40735308565877, 20.772632955377716, 21.096068141197577, 21.379407542992872, 21.624164250773266, 21.831632504709358, 22.00290090643564, 22.138862717583468, 22.240223808140566, 22.307508641393234, 22.341064561482952, 7.944769557821231, 9.924046241510942, 11.441417546161423, 12.701012988734044, 13.797285229027098, 14.776069649903548, 15.661314169224138, 16.466847477758822, 17.20161165502104, 17.872027197474154, 18.48309040522009, 19.038903452778378, 19.542945487578073, 19.998221821354555, 20.407353085658702, 20.772632955377833, 21.096068141197723, 21.379407542993043, 21.624164250773582, 21.831632504709447, 22.00290090643608, 22.138862717585045, 22.240223808142918, 22.307508641395707, 22.341064561485755, 7.944769557821247, 9.92404624151093, 11.441417546161464, 12.701012988733995, 13.79728522902705, 14.776069649903437, 15.661314169223976, 16.466847477758574, 17.201611655020695, 17.87202719747376, 18.483090405219524, 19.038903452777785, 19.542945487577416, 19.998221821353923, 20.407353085658176, 20.772632955377503, 21.09606814119777, 21.379407542993352, 21.624164250774417, 21.831632504710498, 22.00290090643692, 22.138862717586548, 22.240223808145497, 22.307508641398925, 22.341064561489524, 7.9447695578212665, 9.924046241510972, 11.441417546161468, 12.701012988734059, 13.797285229027056, 14.776069649903409, 15.66131416922389, 16.46684747775844, 17.20161165502044, 17.87202719747336, 18.483090405219038, 19.03890345277711, 19.542945487576585, 19.99822182135294, 20.407353085657114, 20.772632955376398, 21.0960681411969, 21.379407542992812, 21.624164250774495, 21.831632504711624, 22.0029009064386, 22.138862717588935, 22.24022380814903, 22.307508641403093, 22.3410645614941, 7.944769557821278, 9.924046241511002, 11.44141754616153, 12.701012988734076, 13.797285229027104, 14.776069649903427, 15.661314169223871, 16.46684747775835, 17.201611655020297, 17.872027197473138, 18.483090405218647, 19.038903452776587, 19.542945487575892, 19.99822182135203, 20.407353085656023, 20.77263295537511, 21.09606814119549, 21.379407542991483, 21.624164250773315, 21.83163250471123, 22.00290090643926, 22.138862717590797, 22.240223808152948, 22.30750864140856, 22.341064561500087, 7.944769557821243, 9.924046241510982, 11.441417546161516, 12.7010129887341, 13.797285229027075, 14.7760696499034, 15.66131416922381, 16.46684747775826, 17.20161165502015, 17.87202719747292, 18.483090405218395, 19.03890345277623, 19.542945487575455, 19.998221821351503, 20.40735308565536, 20.772632955374384, 21.0960681411946, 21.37940754299059, 21.624164250772388, 21.83163250471044, 22.002900906439088, 22.138862717591312, 22.240223808155225, 22.307508641413055, 22.341064561505686, 7.944769557821142, 9.924046241510865, 11.441417546161382, 12.701012988733918, 13.797285229026912, 14.776069649903194, 15.661314169223598, 16.466847477758034, 17.201611655019942, 17.872027197472736, 18.483090405218213, 19.03890345277614, 19.542945487575434, 19.99822182135161, 20.40735308565563, 20.772632955374828, 21.09606814119532, 21.379407542991537, 21.62416425077371, 21.831632504712044, 22.00290090644116, 22.13886271759377, 22.24022380815832, 22.307508641417275, 22.341064561508535]], [[3.776169886144084, 5.273945778726342, 6.267651558979949, 7.059127040042814, 7.7132315748296305, 8.26006903087314, 8.720254447826502, 9.109442969290868, 9.439915499745494, 9.721465126594055, 9.961983347109605, 10.167874469273519, 10.344360701627505, 10.495713517805926, 10.625432946662281, 10.736388626192856, 10.830931883501183, 10.910985309511815, 10.978114512907707, 11.033585542531858, 11.078410628198993, 11.113384274042899, 11.139111268428438, 11.15602780253353, 11.16441658536855, 3.776169886144077, 5.273945778726352, 6.267651558979936, 7.059127040042813, 7.713231574829632, 8.26006903087313, 8.7202544478265, 9.10944296929087, 9.43991549974549, 9.721465126594053, 9.961983347109594, 10.167874469273519, 10.344360701627506, 10.495713517805923, 10.625432946662281, 10.736388626192857, 10.830931883501187, 10.91098530951181, 10.978114512907702, 11.033585542531862, 11.078410628198991, 11.113384274042911, 11.139111268428453, 11.156027802533552, 11.164416585368572, 3.776169886144084, 5.273945778726335, 6.267651558979952, 7.059127040042806, 7.713231574829628, 8.260069030873137, 8.720254447826498, 9.109442969290859, 9.439915499745494, 9.721465126594047, 9.9619833471096, 10.16787446927352, 10.344360701627496, 10.495713517805935, 10.625432946662277, 10.736388626192856, 10.830931883501181, 10.910985309511819, 10.978114512907716, 11.033585542531865, 11.078410628199013, 11.113384274042936, 11.13911126842848, 11.156027802533593, 11.16441658536862, 3.776169886144082, 5.273945778726347, 6.267651558979939, 7.059127040042818, 7.713231574829629, 8.26006903087313, 8.720254447826498, 9.109442969290866, 9.439915499745483, 9.721465126594058, 9.961983347109594, 10.167874469273517, 10.344360701627519, 10.495713517805918, 10.625432946662283, 10.736388626192863, 10.830931883501194, 10.910985309511819, 10.97811451290772, 11.033585542531894, 11.078410628199027, 11.113384274042964, 11.139111268428532, 11.156027802533648, 11.164416585368697, 3.776169886144083, 5.273945778726347, 6.267651558979943, 7.059127040042807, 7.713231574829632, 8.26006903087313, 8.720254447826502, 9.109442969290853, 9.439915499745497, 9.721465126594042, 9.9619833471096, 10.167874469273517, 10.344360701627492, 10.495713517805942, 10.625432946662281, 10.736388626192864, 10.83093188350119, 10.910985309511833, 10.978114512907734, 11.033585542531897, 11.07841062819907, 11.113384274043005, 11.139111268428586, 11.156027802533732, 11.164416585368796, 3.7761698861440807, 5.273945778726338, 6.267651558979949, 7.059127040042802, 7.713231574829628, 8.260069030873135, 8.720254447826491, 9.109442969290871, 9.439915499745481, 9.721465126594063, 9.961983347109587, 10.167874469273515, 10.344360701627517, 10.495713517805921, 10.625432946662295, 10.736388626192868, 10.830931883501204, 10.91098530951183, 10.978114512907753, 11.033585542531936, 11.078410628199089, 11.113384274043062, 11.139111268428664, 11.156027802533817, 11.164416585368905, 3.776169886144083, 5.273945778726348, 6.267651558979933, 7.059127040042818, 7.713231574829619, 8.260069030873126, 8.720254447826509, 9.109442969290846, 9.439915499745505, 9.721465126594039, 9.961983347109598, 10.167874469273515, 10.344360701627501, 10.495713517805942, 10.625432946662281, 10.736388626192873, 10.830931883501195, 10.91098530951186, 10.978114512907766, 11.033585542531938, 11.07841062819914, 11.11338427404311, 11.139111268428731, 11.156027802533933, 11.164416585369013, 3.776169886144076, 5.27394577872634, 6.267651558979951, 7.059127040042796, 7.71323157482964, 8.26006903087312, 8.720254447826491, 9.10944296929088, 9.439915499745466, 9.721465126594067, 9.961983347109582, 10.167874469273508, 10.34436070162751, 10.49571351780592, 10.625432946662295, 10.736388626192863, 10.830931883501215, 10.91098530951185, 10.97811451290778, 11.033585542531968, 11.078410628199146, 11.113384274043163, 11.13911126842882, 11.15602780253405, 11.16441658536914, 3.7761698861440816, 5.2739457787263495, 6.267651558979933, 7.059127040042817, 7.713231574829614, 8.260069030873138, 8.720254447826495, 9.109442969290845, 9.439915499745506, 9.721465126594024, 9.961983347109598, 10.167874469273503, 10.344360701627501, 10.495713517805928, 10.625432946662265, 10.736388626192879, 10.8309318835012, 10.910985309511872, 10.978114512907775, 11.033585542531972, 11.078410628199194, 11.113384274043202, 11.139111268428895, 11.15602780253417, 11.164416585369244, 3.7761698861440745, 5.273945778726336, 6.267651558979952, 7.059127040042791, 7.713231574829636, 8.260069030873117, 8.720254447826497, 9.109442969290868, 9.43991549974546, 9.721465126594069, 9.961983347109564, 10.167874469273507, 10.34436070162749, 10.495713517805918, 10.625432946662281, 10.736388626192847, 10.830931883501211, 10.91098530951185, 10.978114512907796, 11.033585542531991, 11.078410628199197, 11.113384274043254, 11.139111268428964, 11.156027802534277, 11.164416585369338, 3.7761698861440847, 5.273945778726345, 6.2676515589799315, 7.059127040042819, 7.713231574829608, 8.260069030873138, 8.720254447826484, 9.109442969290852, 9.439915499745492, 9.721465126594017, 9.961983347109596, 10.167874469273485, 10.344360701627485, 10.495713517805907, 10.62543294666226, 10.736388626192861, 10.830931883501181, 10.910985309511863, 10.978114512907759, 11.033585542531982, 11.078410628199222, 11.113384274043264, 11.139111268429028, 11.156027802534378, 11.164416585369391, 3.7761698861440767, 5.273945778726336, 6.267651558979953, 7.0591270400427915, 7.713231574829637, 8.260069030873115, 8.720254447826497, 9.109442969290857, 9.439915499745467, 9.721465126594046, 9.961983347109554, 10.167874469273505, 10.344360701627457, 10.495713517805909, 10.625432946662253, 10.736388626192815, 10.83093188350118, 10.910985309511823, 10.978114512907773, 11.033585542531952, 11.078410628199185, 11.113384274043284, 11.139111268429053, 11.15602780253444, 11.164416585369409, 3.7761698861440864, 5.273945778726351, 6.267651558979923, 7.059127040042827, 7.713231574829603, 8.260069030873138, 8.720254447826484, 9.109442969290846, 9.439915499745478, 9.721465126594017, 9.961983347109571, 10.167874469273466, 10.344360701627462, 10.495713517805862, 10.625432946662244, 10.736388626192813, 10.830931883501133, 10.910985309511812, 10.978114512907702, 11.033585542531933, 11.078410628199158, 11.113384274043236, 11.139111268429065, 11.156027802534478, 11.164416585369349, 3.7761698861440642, 5.273945778726343, 6.267651558979954, 7.059127040042786, 7.713231574829648, 8.260069030873103, 8.7202544478265, 9.109442969290841, 9.439915499745457, 9.721465126594033, 9.961983347109536, 10.167874469273485, 10.34436070162743, 10.495713517805864, 10.625432946662185, 10.736388626192788, 10.830931883501114, 10.910985309511767, 10.97811451290771, 11.033585542531837, 11.078410628199094, 11.113384274043208, 11.139111268429016, 11.156027802534453, 11.16441658536923, 3.7761698861441015, 5.273945778726337, 6.26765155897994, 7.059127040042815, 7.713231574829611, 8.260069030873145, 8.720254447826468, 9.109442969290862, 9.439915499745442, 9.721465126594007, 9.96198334710955, 10.167874469273432, 10.34436070162745, 10.495713517805832, 10.625432946662183, 10.736388626192738, 10.83093188350107, 10.910985309511716, 10.978114512907641, 11.033585542531837, 11.078410628198984, 11.113384274043076, 11.13911126842894, 11.156027802534362, 11.164416585369004, 3.7761698861440745, 5.27394577872635, 6.26765155897995, 7.059127040042805, 7.71323157482963, 8.260069030873126, 8.720254447826493, 9.10944296929084, 9.439915499745467, 9.721465126593989, 9.961983347109546, 10.167874469273428, 10.3443607016274, 10.49571351780583, 10.625432946662142, 10.736388626192747, 10.830931883501016, 10.910985309511677, 10.978114512907586, 11.033585542531698, 11.0784106281989, 11.113384274042952, 11.139111268428783, 11.156027802534203, 11.164416585368691, 3.776169886144096, 5.273945778726354, 6.267651558979941, 7.059127040042831, 7.713231574829615, 8.260069030873137, 8.720254447826482, 9.109442969290843, 9.43991549974545, 9.721465126593987, 9.961983347109529, 10.167874469273427, 10.344360701627375, 10.495713517805806, 10.625432946662118, 10.73638862619267, 10.830931883501009, 10.910985309511565, 10.978114512907554, 11.03358554253169, 11.07841062819869, 11.11338427404273, 11.139111268428591, 11.156027802533966, 11.16441658536825, 3.776169886144077, 5.273945778726366, 6.267651558979965, 7.059127040042807, 7.713231574829651, 8.260069030873117, 8.720254447826505, 9.109442969290825, 9.439915499745458, 9.721465126593989, 9.961983347109506, 10.167874469273423, 10.344360701627375, 10.495713517805777, 10.625432946662109, 10.736388626192648, 10.830931883500952, 10.91098530951154, 10.978114512907371, 11.033585542531622, 11.078410628198663, 11.113384274042472, 11.139111268428273, 11.156027802533634, 11.164416585367725, 3.776169886144126, 5.273945778726352, 6.267651558979975, 7.059127040042826, 7.7132315748296385, 8.260069030873145, 8.720254447826486, 9.109442969290864, 9.439915499745434, 9.721465126594012, 9.961983347109495, 10.167874469273409, 10.34436070162735, 10.49571351780576, 10.625432946662073, 10.736388626192609, 10.830931883500963, 10.910985309511503, 10.978114512907359, 11.03358554253146, 11.078410628198458, 11.11338427404223, 11.139111268427923, 11.156027802533234, 11.164416585367078, 3.776169886144095, 5.273945778726392, 6.267651558979968, 7.059127040042849, 7.7132315748296465, 8.260069030873163, 8.720254447826495, 9.109442969290862, 9.43991549974546, 9.721465126594, 9.96198334710952, 10.167874469273396, 10.344360701627384, 10.495713517805697, 10.625432946662094, 10.736388626192536, 10.830931883500858, 10.910985309511519, 10.978114512907222, 11.033585542531524, 11.078410628198457, 11.113384274041884, 11.139111268427385, 11.15602780253272, 11.164416585366387, 3.776169886144133, 5.273945778726387, 6.2676515589799955, 7.059127040042856, 7.713231574829676, 8.260069030873158, 8.720254447826528, 9.109442969290866, 9.439915499745497, 9.721465126594001, 9.961983347109577, 10.167874469273405, 10.344360701627403, 10.495713517805784, 10.625432946662036, 10.736388626192658, 10.830931883500734, 10.910985309511435, 10.978114512907133, 11.033585542531094, 11.078410628198512, 11.113384274041865, 11.139111268426921, 11.156027802532105, 11.1644165853656, 3.776169886144131, 5.273945778726416, 6.267651558980014, 7.059127040042875, 7.713231574829702, 8.260069030873185, 8.720254447826557, 9.109442969290901, 9.439915499745517, 9.721465126594067, 9.961983347109557, 10.16787446927352, 10.344360701627403, 10.495713517805898, 10.625432946662144, 10.736388626192726, 10.830931883500982, 10.910985309511412, 10.97811451290732, 11.033585542530917, 11.078410628197926, 11.113384274041646, 11.139111268426337, 11.156027802531543, 11.164416585365123, 3.7761698861441575, 5.2739457787264215, 6.2676515589800434, 7.0591270400429185, 7.713231574829725, 8.260069030873243, 8.720254447826589, 9.109442969290974, 9.439915499745558, 9.721465126594136, 9.961983347109658, 10.16787446927356, 10.344360701627568, 10.495713517805964, 10.625432946662368, 10.73638862619287, 10.830931883501291, 10.910985309511759, 10.978114512907661, 11.033585542531535, 11.078410628198085, 11.11338427404155, 11.139111268425845, 11.156027802530426, 11.164416585364775, 3.7761698861441486, 5.273945778726457, 6.267651558980061, 7.059127040042944, 7.713231574829781, 8.26006903087328, 8.720254447826676, 9.10944296929104, 9.439915499745698, 9.721465126594245, 9.961983347109827, 10.167874469273757, 10.344360701627785, 10.495713517806236, 10.625432946662658, 10.736388626193252, 10.830931883501659, 10.910985309512363, 10.978114512908208, 11.033585542532451, 11.078410628199155, 11.113384274042794, 11.139111268427017, 11.156027802531014, 11.164416585366194, 3.776169886144034, 5.273945778726313, 6.267651558979996, 7.059127040042904, 7.713231574829774, 8.26006903087335, 8.720254447826772, 9.109442969291223, 9.439915499745902, 9.721465126594566, 9.96198334711019, 10.167874469274215, 10.344360701628329, 10.495713517806895, 10.625432946663375, 10.73638862619416, 10.830931883502616, 10.910985309513519, 10.978114512909515, 11.033585542533919, 11.078410628201127, 11.113384274044956, 11.13911126843046, 11.156027802534204, 11.164416585374632]]]

        phi_test = np.array(phi_test)

        # Test the scalar flux
        l = 0
        phi = pydgm.state.mg_phi[l, :, :].flatten()
        phi_zero_test = phi_test[:, l].flatten()
        np.testing.assert_array_almost_equal(phi, phi_zero_test, 7)

        self.angular_test()

    # @unittest.skipIf(anisotropicBroken, 'Anisotropic is not working yet')
    def test_solver_basic_2D_2g_8a_vacuum_l2(self):
        '''
        Test for a basic 2 group problem
        '''
        self.set_mesh('simple')
        pydgm.control.material_map = [2]
        pydgm.control.angle_order = 8
        pydgm.control.boundary_east = 1.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0
        pydgm.control.allow_fission = False
        pydgm.control.scatter_leg_order = 2

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[7.928479727938278, 9.92490986328297, 11.466671812411317, 12.74450044108161, 13.85151589614638, 14.835209613662713, 15.721410514272677, 16.525400133977776, 17.257119619690425, 17.923648015136497, 18.530410772929663, 19.081790352350684, 19.581450091621544, 20.032516800652697, 20.437691008536852, 20.799318226674295, 21.119437864235163, 21.399818436179324, 21.64198378428386, 21.84723304175064, 22.0166560140035, 22.151145053167696, 22.251404147219485, 22.317955716948806, 22.351145458739975, 7.928479727938263, 9.924909863283004, 11.466671812411294, 12.744500441081623, 13.851515896146392, 14.8352096136627, 15.721410514272687, 16.525400133977787, 17.257119619690435, 17.923648015136504, 18.53041077292967, 19.081790352350698, 19.58145009162157, 20.032516800652694, 20.437691008536845, 20.799318226674284, 21.119437864235163, 21.399818436179306, 21.64198378428383, 21.8472330417506, 22.016656014003434, 22.15114505316759, 22.25140414721936, 22.31795571694865, 22.351145458739804, 7.9284797279383055, 9.924909863282947, 11.466671812411352, 12.74450044108163, 13.851515896146397, 14.835209613662741, 15.721410514272696, 16.525400133977783, 17.257119619690442, 17.92364801513653, 18.530410772929685, 19.081790352350712, 19.581450091621573, 20.0325168006527, 20.437691008536856, 20.79931822667427, 21.119437864235127, 21.39981843617929, 21.641983784283774, 21.84723304175049, 22.016656014003278, 22.15114505316739, 22.2514041472191, 22.317955716948358, 22.35114545873946, 7.92847972793828, 9.924909863283036, 11.466671812411303, 12.744500441081668, 13.851515896146424, 14.835209613662746, 15.721410514272742, 16.525400133977808, 17.257119619690478, 17.92364801513655, 18.530410772929713, 19.081790352350726, 19.581450091621623, 20.032516800652743, 20.437691008536827, 20.799318226674266, 21.11943786423514, 21.399818436179228, 21.6419837842837, 21.84723304175035, 22.016656014003043, 22.151145053167095, 22.25140414721873, 22.3179557169479, 22.351145458738948, 7.928479727938324, 9.924909863282984, 11.46667181241138, 12.744500441081662, 13.85151589614644, 14.835209613662796, 15.721410514272764, 16.525400133977843, 17.257119619690503, 17.923648015136585, 18.530410772929745, 19.081790352350755, 19.581450091621626, 20.032516800652758, 20.43769100853686, 20.79931822667424, 21.119437864235096, 21.39981843617923, 21.6419837842836, 21.84723304175016, 22.016656014002773, 22.151145053166697, 22.251404147218228, 22.317955716947306, 22.351145458738312, 7.928479727938294, 9.924909863283064, 11.46667181241136, 12.744500441081708, 13.851515896146482, 14.83520961366281, 15.721410514272803, 16.525400133977886, 17.25711961969053, 17.923648015136617, 18.53041077292979, 19.081790352350787, 19.581450091621686, 20.032516800652814, 20.437691008536845, 20.79931822667424, 21.119437864235106, 21.399818436179153, 21.641983784283504, 21.84723304174997, 22.016656014002432, 22.151145053166232, 22.251404147217638, 22.317955716946603, 22.35114545873751, 7.928479727938353, 9.924909863283014, 11.466671812411423, 12.744500441081735, 13.851515896146497, 14.835209613662855, 15.721410514272844, 16.52540013397793, 17.257119619690606, 17.92364801513668, 18.53041077292981, 19.08179035235084, 19.581450091621704, 20.032516800652836, 20.437691008536884, 20.79931822667421, 21.11943786423503, 21.399818436179135, 21.641983784283397, 21.847233041749732, 22.016656014002063, 22.1511450531657, 22.251404147216945, 22.317955716945793, 22.35114545873661, 7.9284797279383215, 9.92490986328311, 11.4666718124114, 12.744500441081742, 13.851515896146571, 14.835209613662872, 15.72141051427287, 16.525400133978, 17.25711961969063, 17.923648015136735, 18.5304107729299, 19.08179035235085, 19.581450091621722, 20.03251680065287, 20.437691008536895, 20.799318226674213, 21.119437864235017, 21.399818436179046, 21.641983784283294, 21.847233041749515, 22.016656014001647, 22.151145053165106, 22.25140414721618, 22.317955716944873, 22.351145458735623, 7.928479727938388, 9.92490986328305, 11.466671812411475, 12.744500441081772, 13.851515896146541, 14.835209613662963, 15.721410514272904, 16.52540013397802, 17.257119619690737, 17.923648015136767, 18.53041077292993, 19.081790352350946, 19.58145009162177, 20.032516800652882, 20.43769100853692, 20.799318226674192, 21.119437864234957, 21.399818436179025, 21.641983784283173, 21.847233041749252, 22.01665601400123, 22.151145053164473, 22.251404147215368, 22.31795571694392, 22.351145458734567, 7.928479727938358, 9.924909863283148, 11.466671812411438, 12.744500441081804, 13.851515896146614, 14.835209613662922, 15.721410514272977, 16.525400133978074, 17.257119619690755, 17.923648015136866, 18.53041077292999, 19.081790352350975, 19.58145009162179, 20.03251680065289, 20.43769100853693, 20.799318226674185, 21.11943786423491, 21.39981843617891, 21.641983784283067, 21.84723304174905, 22.016656014000805, 22.15114505316383, 22.25140414721451, 22.317955716942908, 22.3511454587335, 7.9284797279384325, 9.9249098632831, 11.466671812411525, 12.744500441081827, 13.851515896146617, 14.83520961366301, 15.721410514272957, 16.525400133978117, 17.25711961969079, 17.923648015136866, 18.530410772930075, 19.081790352351046, 19.581450091621846, 20.032516800652886, 20.43769100853692, 20.799318226674178, 21.11943786423483, 21.399818436178833, 21.641983784282942, 21.847233041748837, 22.016656014000436, 22.151145053163194, 22.251404147213666, 22.317955716941906, 22.35114545873244, 7.9284797279384, 9.924909863283188, 11.466671812411482, 12.74450044108188, 13.851515896146655, 14.835209613662993, 15.721410514273053, 16.525400133978113, 17.257119619690833, 17.923648015136898, 18.53041077293004, 19.08179035235112, 19.58145009162186, 20.032516800652896, 20.437691008536916, 20.799318226674135, 21.11943786423477, 21.39981843617868, 21.641983784282857, 21.84723304174868, 22.016656014000084, 22.15114505316263, 22.25140414721283, 22.31795571694093, 22.351145458731455, 7.928479727938447, 9.924909863283153, 11.46667181241156, 12.744500441081863, 13.851515896146678, 14.83520961366304, 15.721410514273021, 16.525400133978167, 17.25711961969081, 17.923648015136944, 18.530410772930065, 19.081790352351057, 19.58145009162194, 20.032516800652843, 20.43769100853686, 20.799318226674114, 21.11943786423467, 21.399818436178574, 21.64198378428268, 21.847233041748567, 22.01665601399985, 22.15114505316211, 22.25140414721209, 22.31795571694004, 22.351145458730574, 7.928479727938421, 9.924909863283203, 11.466671812411535, 12.744500441081906, 13.851515896146687, 14.835209613663029, 15.721410514273066, 16.52540013397814, 17.25711961969082, 17.923648015136898, 18.53041077293005, 19.08179035235103, 19.581450091621846, 20.032516800652903, 20.43769100853675, 20.799318226674, 21.11943786423458, 21.3998184361784, 21.641983784282576, 21.847233041748442, 22.01665601399966, 22.15114505316175, 22.251404147211463, 22.317955716939288, 22.35114545872987, 7.928479727938472, 9.924909863283167, 11.466671812411583, 12.74450044108187, 13.8515158961467, 14.835209613663057, 15.721410514273007, 16.525400133978174, 17.257119619690766, 17.923648015136862, 18.53041077293, 19.081790352350925, 19.58145009162176, 20.03251680065278, 20.437691008536735, 20.799318226673858, 21.119437864234435, 21.399818436178222, 21.641983784282342, 21.84723304174841, 22.01665601399962, 22.15114505316149, 22.251404147211005, 22.317955716938712, 22.351145458729384, 7.928479727938451, 9.92490986328322, 11.466671812411542, 12.744500441081925, 13.851515896146642, 14.83520961366302, 15.721410514273025, 16.525400133978064, 17.25711961969078, 17.92364801513677, 18.530410772929915, 19.081790352350826, 19.581450091621587, 20.032516800652594, 20.437691008536504, 20.799318226673766, 21.119437864234282, 21.399818436178045, 21.641983784282175, 21.847233041748257, 22.01665601399967, 22.15114505316149, 22.251404147210764, 22.317955716938368, 22.351145458729192, 7.928479727938474, 9.924909863283208, 11.46667181241158, 12.74450044108187, 13.851515896146676, 14.835209613662967, 15.72141051427293, 16.52540013397803, 17.257119619690606, 17.923648015136656, 18.530410772929745, 19.081790352350673, 19.581450091621388, 20.032516800652402, 20.43769100853627, 20.799318226673414, 21.119437864234133, 21.399818436177814, 21.6419837842819, 21.847233041748236, 22.01665601399975, 22.15114505316164, 22.25140414721083, 22.317955716938332, 22.351145458729338, 7.928479727938449, 9.924909863283208, 11.466671812411546, 12.744500441081886, 13.851515896146596, 14.83520961366293, 15.721410514272877, 16.52540013397786, 17.257119619690503, 17.923648015136468, 18.530410772929496, 19.081790352350403, 19.581450091621114, 20.032516800652054, 20.43769100853603, 20.799318226673122, 21.119437864233756, 21.399818436177686, 21.641983784281624, 21.847233041747984, 22.01665601400004, 22.15114505316209, 22.251404147211183, 22.31795571693868, 22.351145458729896, 7.928479727938441, 9.924909863283174, 11.466671812411528, 12.744500441081783, 13.851515896146562, 14.835209613662807, 15.721410514272725, 16.525400133977765, 17.257119619690247, 17.923648015136237, 18.53041077292923, 19.081790352350037, 19.581450091620734, 20.032516800651663, 20.437691008535534, 20.79931822667275, 21.119437864233362, 21.399818436177316, 21.641983784281578, 21.847233041747852, 22.01665601400013, 22.151145053162796, 22.25140414721202, 22.31795571693947, 22.351145458730933, 7.928479727938441, 9.924909863283169, 11.466671812411477, 12.744500441081755, 13.851515896146395, 14.835209613662677, 15.721410514272513, 16.52540013397742, 17.257119619689966, 17.92364801513584, 18.530410772928793, 19.081790352349618, 19.581450091620265, 20.032516800651162, 20.437691008535083, 20.79931822667225, 21.119437864232935, 21.399818436176936, 21.641983784281233, 21.847233041747913, 22.01665601400051, 22.15114505316362, 22.251404147213304, 22.31795571694088, 22.351145458732574, 7.928479727938482, 9.924909863283212, 11.466671812411485, 12.744500441081684, 13.851515896146362, 14.835209613662476, 15.721410514272256, 16.525400133977126, 17.257119619689476, 17.92364801513531, 18.53041077292821, 19.081790352348925, 19.58145009161959, 20.032516800650498, 20.437691008534447, 20.79931822667177, 21.11943786423251, 21.399818436176744, 21.641983784281116, 21.847233041747735, 22.016656014000944, 22.151145053164846, 22.251404147215126, 22.31795571694302, 22.35114545873502, 7.928479727938561, 9.924909863283272, 11.466671812411542, 12.744500441081728, 13.851515896146278, 14.835209613662405, 15.721410514272064, 16.525400133976778, 17.257119619689107, 17.923648015134734, 18.530410772927482, 19.08179035234811, 19.581450091618606, 20.0325168006495, 20.43769100853346, 20.799318226670906, 21.119437864231923, 21.399818436176435, 21.64198378428144, 21.847233041748233, 22.016656014001505, 22.1511450531664, 22.251404147217617, 22.317955716946056, 22.351145458738635, 7.928479727938631, 9.924909863283355, 11.466671812411601, 12.744500441081763, 13.851515896146337, 14.835209613662327, 15.721410514271957, 16.525400133976614, 17.25711961968872, 17.92364801513429, 18.53041077292685, 19.081790352347294, 19.58145009161765, 20.032516800648377, 20.437691008532266, 20.799318226669676, 21.119437864230918, 21.399818436175703, 21.641983784281315, 21.84723304174918, 22.016656014003008, 22.151145053168726, 22.251404147221418, 22.317955716950593, 22.351145458743787, 7.928479727938694, 9.924909863283412, 11.466671812411652, 12.744500441081783, 13.851515896146264, 14.835209613662283, 15.721410514271792, 16.525400133976365, 17.257119619688478, 17.923648015133868, 18.53041077292638, 19.081790352346726, 19.581450091616986, 20.032516800647638, 20.437691008531473, 20.799318226668856, 21.119437864230168, 21.399818436175227, 21.641983784281187, 21.84723304174992, 22.01665601400499, 22.15114505317193, 22.251404147226562, 22.317955716957872, 22.35114545875216, 7.9284797279388055, 9.924909863283428, 11.466671812411578, 12.744500441081659, 13.851515896146108, 14.835209613662022, 15.721410514271572, 16.525400133976117, 17.257119619688194, 17.923648015133683, 18.53041077292621, 19.081790352346648, 19.581450091617054, 20.03251680064785, 20.437691008531885, 20.79931822666958, 21.11943786423121, 21.399818436176734, 21.641983784283273, 21.847233041752766, 22.016656014008888, 22.151145053177167, 22.251404147233593, 22.317955716966857, 22.351145458763856]], [[3.777058744550611, 5.284461450947354, 6.284610743985109, 7.076116309958862, 7.728436938718256, 8.27316632614082, 8.731361235639728, 9.118809381488354, 9.44781488753294, 9.728150687511656, 9.967672664349713, 10.172747072226075, 10.348561454048054, 10.499358153813674, 10.628613920819484, 10.739180439444755, 10.83339557298747, 10.91317205545358, 10.980068438115723, 11.035345826607166, 11.08001306675826, 11.114862403949843, 11.140497164118814, 11.157352631803924, 11.165710998258144, 3.7770587445505948, 5.284461450947384, 6.284610743985083, 7.076116309958866, 7.728436938718261, 8.273166326140814, 8.73136123563973, 9.118809381488362, 9.447814887532935, 9.72815068751165, 9.967672664349701, 10.17274707222607, 10.348561454048069, 10.499358153813665, 10.628613920819474, 10.739180439444755, 10.833395572987484, 10.913172055453574, 10.980068438115701, 11.035345826607172, 11.08001306675825, 11.114862403949825, 11.140497164118806, 11.15735263180391, 11.165710998258136, 3.777058744550617, 5.284461450947337, 6.2846107439851195, 7.076116309958851, 7.728436938718254, 8.273166326140824, 8.731361235639726, 9.118809381488349, 9.447814887532937, 9.728150687511643, 9.96767266434971, 10.172747072226075, 10.348561454048035, 10.499358153813674, 10.628613920819479, 10.739180439444748, 10.833395572987454, 10.913172055453575, 10.980068438115708, 11.035345826607138, 11.080013066758239, 11.114862403949818, 11.14049716411879, 11.1573526318039, 11.165710998258122, 3.777058744550598, 5.284461450947375, 6.284610743985082, 7.076116309958877, 7.728436938718252, 8.273166326140814, 8.731361235639728, 9.118809381488358, 9.447814887532921, 9.728150687511652, 9.967672664349692, 10.172747072226061, 10.34856145404807, 10.499358153813645, 10.628613920819458, 10.739180439444734, 10.833395572987476, 10.913172055453552, 10.980068438115673, 11.035345826607154, 11.080013066758218, 11.114862403949795, 11.14049716411877, 11.157352631803882, 11.1657109982581, 3.777058744550618, 5.284461450947354, 6.284610743985107, 7.076116309958853, 7.728436938718262, 8.273166326140807, 8.731361235639724, 9.11880938148834, 9.447814887532939, 9.728150687511636, 9.967672664349703, 10.172747072226075, 10.34856145404803, 10.499358153813672, 10.628613920819461, 10.739180439444732, 10.833395572987428, 10.913172055453565, 10.980068438115683, 11.035345826607099, 11.080013066758216, 11.114862403949775, 11.140497164118736, 11.157352631803855, 11.165710998258076, 3.7770587445505983, 5.284461450947369, 6.284610743985102, 7.076116309958861, 7.728436938718254, 8.273166326140823, 8.731361235639712, 9.118809381488358, 9.447814887532912, 9.728150687511656, 9.967672664349694, 10.17274707222606, 10.348561454048061, 10.499358153813635, 10.628613920819456, 10.739180439444715, 10.833395572987465, 10.913172055453515, 10.980068438115643, 11.035345826607116, 11.080013066758166, 11.114862403949745, 11.140497164118718, 11.15735263180382, 11.16571099825805, 3.7770587445506245, 5.284461450947359, 6.284610743985102, 7.076116309958874, 7.728436938718247, 8.27316632614081, 8.73136123563974, 9.118809381488326, 9.44781488753295, 9.728150687511627, 9.967672664349701, 10.172747072226061, 10.348561454048033, 10.499358153813667, 10.628613920819431, 10.739180439444722, 10.83339557298741, 10.913172055453545, 10.98006843811565, 11.03534582660705, 11.08001306675817, 11.11486240394972, 11.140497164118674, 11.157352631803793, 11.165710998258009, 3.7770587445506, 5.284461450947377, 6.2846107439851036, 7.076116309958858, 7.728436938718272, 8.273166326140805, 8.731361235639712, 9.118809381488376, 9.447814887532907, 9.728150687511667, 9.967672664349692, 10.172747072226057, 10.348561454048038, 10.499358153813633, 10.628613920819456, 10.739180439444686, 10.833395572987438, 10.913172055453476, 10.980068438115616, 11.035345826607081, 11.080013066758104, 11.114862403949688, 11.140497164118658, 11.15735263180375, 11.165710998257984, 3.7770587445506254, 5.284461450947359, 6.284610743985107, 7.076116309958874, 7.728436938718241, 8.273166326140833, 8.73136123563973, 9.118809381488328, 9.447814887532967, 9.728150687511617, 9.967672664349712, 10.17274707222605, 10.348561454048042, 10.499358153813642, 10.628613920819399, 10.739180439444713, 10.833395572987381, 10.913172055453503, 10.980068438115588, 11.035345826607, 11.08001306675812, 11.114862403949646, 11.1404971641186, 11.157352631803729, 11.165710998257945, 3.7770587445505974, 5.2844614509473775, 6.2846107439851115, 7.076116309958858, 7.728436938718279, 8.273166326140803, 8.731361235639733, 9.118809381488365, 9.447814887532903, 9.728150687511675, 9.967672664349672, 10.172747072226057, 10.348561454048006, 10.499358153813638, 10.628613920819438, 10.739180439444647, 10.833395572987401, 10.91317205545343, 10.980068438115579, 11.035345826607013, 11.080013066758028, 11.114862403949632, 11.14049716411859, 11.157352631803677, 11.165710998257916, 3.777058744550631, 5.284461450947362, 6.284610743985109, 7.076116309958883, 7.728436938718244, 8.27316632614084, 8.731361235639719, 9.118809381488353, 9.447814887532955, 9.728150687511615, 9.96767266434972, 10.172747072226024, 10.348561454048035, 10.4993581538136, 10.628613920819385, 10.73918043944469, 10.833395572987335, 10.913172055453462, 10.980068438115493, 11.035345826606942, 11.080013066758063, 11.114862403949566, 11.140497164118534, 11.157352631803663, 11.165710998257877, 3.777058744550603, 5.284461450947378, 6.284610743985117, 7.076116309958859, 7.728436938718284, 8.273166326140803, 8.731361235639742, 9.118809381488356, 9.447814887532926, 9.728150687511658, 9.967672664349665, 10.172747072226066, 10.348561454047974, 10.499358153813631, 10.628613920819385, 10.739180439444599, 10.83339557298735, 10.913172055453384, 10.980068438115536, 11.035345826606898, 11.080013066757944, 11.114862403949578, 11.140497164118516, 11.157352631803606, 11.165710998257843, 3.7770587445506343, 5.284461450947373, 6.2846107439851036, 7.076116309958894, 7.728436938718239, 8.273166326140846, 8.731361235639714, 9.118809381488353, 9.447814887532944, 9.728150687511624, 9.967672664349701, 10.172747072226, 10.348561454048017, 10.499358153813548, 10.628613920819394, 10.739180439444635, 10.833395572987284, 10.9131720554534, 10.980068438115408, 11.035345826606887, 11.080013066757958, 11.11486240394946, 11.14049716411847, 11.157352631803592, 11.16571099825778, 3.7770587445505854, 5.284461450947394, 6.284610743985118, 7.076116309958862, 7.7284369387182945, 8.273166326140789, 8.731361235639762, 9.11880938148833, 9.447814887532928, 9.72815068751164, 9.96767266434965, 10.172747072226056, 10.348561454047957, 10.499358153813573, 10.62861392081931, 10.7391804394446, 10.83339557298728, 10.913172055453334, 10.980068438115469, 11.035345826606742, 11.080013066757836, 11.114862403949486, 11.140497164118411, 11.15735263180351, 11.165710998257723, 3.7770587445506494, 5.284461450947354, 6.284610743985129, 7.076116309958875, 7.728436938718255, 8.273166326140846, 8.731361235639694, 9.11880938148838, 9.447814887532886, 9.728150687511624, 9.967672664349656, 10.172747072225976, 10.348561454048015, 10.499358153813526, 10.628613920819339, 10.739180439444526, 10.83339557298723, 10.913172055453286, 10.98006843811534, 11.035345826606807, 11.080013066757747, 11.1148624039493, 11.140497164118372, 11.157352631803471, 11.165710998257566, 3.7770587445506005, 5.28446145094739, 6.2846107439851115, 7.076116309958877, 7.72843693871827, 8.273166326140812, 8.731361235639735, 9.118809381488317, 9.447814887532923, 9.728150687511588, 9.967672664349653, 10.172747072225972, 10.348561454047928, 10.499358153813546, 10.628613920819253, 10.739180439444572, 10.833395572987152, 10.91317205545325, 10.980068438115316, 11.03534582660657, 11.080013066757694, 11.114862403949274, 11.140497164118202, 11.15735263180332, 11.165710998257374, 3.7770587445506396, 5.284461450947371, 6.284610743985117, 7.076116309958885, 7.728436938718254, 8.273166326140831, 8.731361235639696, 9.118809381488342, 9.447814887532884, 9.7281506875116, 9.967672664349633, 10.172747072225976, 10.348561454047902, 10.499358153813507, 10.628613920819246, 10.739180439444436, 10.83339557298718, 10.913172055453101, 10.980068438115307, 11.035345826606664, 11.080013066757395, 11.114862403949008, 11.14049716411813, 11.15735263180317, 11.165710998256978, 3.7770587445505925, 5.284461450947407, 6.284610743985107, 7.076116309958881, 7.7284369387182705, 8.273166326140792, 8.731361235639735, 9.118809381488282, 9.447814887532903, 9.728150687511565, 9.967672664349598, 10.17274707222594, 10.348561454047896, 10.499358153813452, 10.628613920819232, 10.739180439444457, 10.833395572987055, 10.913172055453114, 10.980068438115037, 11.035345826606534, 11.08001306675752, 11.114862403948791, 11.140497164117749, 11.157352631802883, 11.1657109982565, 3.777058744550659, 5.284461450947356, 6.284610743985153, 7.076116309958859, 7.728436938718283, 8.273166326140805, 8.731361235639694, 9.118809381488333, 9.447814887532846, 9.72815068751158, 9.967672664349562, 10.172747072225931, 10.34856145404781, 10.499358153813445, 10.628613920819136, 10.739180439444386, 10.833395572987113, 10.913172055453003, 10.980068438115135, 11.035345826606324, 11.080013066757148, 11.114862403948617, 11.140497164117559, 11.157352631802505, 11.165710998255639, 3.7770587445506143, 5.284461450947413, 6.284610743985104, 7.076116309958908, 7.728436938718247, 8.273166326140833, 8.731361235639692, 9.118809381488317, 9.447814887532859, 9.72815068751157, 9.967672664349564, 10.172747072225896, 10.34856145404787, 10.499358153813304, 10.628613920819184, 10.739180439444205, 10.83339557298697, 10.913172055453012, 10.980068438114868, 11.035345826606614, 11.08001306675725, 11.114862403948125, 11.140497164116978, 11.157352631802086, 11.165710998254768, 3.777058744550645, 5.284461450947393, 6.284610743985144, 7.076116309958884, 7.728436938718282, 8.27316632614081, 8.73136123563971, 9.118809381488306, 9.44781488753288, 9.728150687511526, 9.967672664349648, 10.172747072225862, 10.348561454047893, 10.499358153813407, 10.6286139208191, 10.739180439444395, 10.83339557298675, 10.913172055452977, 10.980068438114694, 11.035345826605983, 11.080013066757568, 11.114862403948372, 11.140497164116653, 11.157352631801485, 11.165710998253571, 3.777058744550648, 5.284461450947419, 6.284610743985145, 7.076116309958907, 7.728436938718289, 8.273166326140824, 8.731361235639733, 9.118809381488301, 9.447814887532896, 9.728150687511585, 9.967672664349578, 10.172747072225993, 10.348561454047848, 10.49935815381354, 10.628613920819186, 10.739180439444524, 10.833395572987085, 10.913172055452991, 10.98006843811512, 11.035345826605795, 11.080013066756898, 11.114862403948425, 11.140497164116422, 11.157352631801434, 11.16571099825309, 3.777058744550669, 5.284461450947425, 6.284610743985178, 7.07611630995893, 7.728436938718318, 8.273166326140876, 8.731361235639742, 9.11880938148839, 9.4478148875329, 9.728150687511647, 9.96767266434966, 10.172747072226006, 10.34856145404798, 10.49935815381357, 10.628613920819415, 10.73918043944463, 10.833395572987504, 10.913172055453423, 10.980068438115714, 11.03534582660688, 11.080013066757468, 11.11486240394882, 11.140497164116754, 11.1573526318011, 11.165710998253484, 3.7770587445506836, 5.284461450947469, 6.2846107439851995, 7.076116309958985, 7.728436938718369, 8.273166326140936, 8.731361235639845, 9.118809381488438, 9.447814887533061, 9.72815068751173, 9.967672664349827, 10.172747072226182, 10.348561454048205, 10.499358153813805, 10.62861392081972, 10.739180439445018, 10.833395572987897, 10.913172055454124, 10.980068438116398, 11.035345826608195, 11.08001306675914, 11.114862403951095, 11.140497164119394, 11.157352631804319, 11.165710998257598, 3.777058744550701, 5.284461450947475, 6.284610743985255, 7.076116309959026, 7.728436938718467, 8.273166326141054, 8.731361235640007, 9.118809381488685, 9.447814887533301, 9.728150687512118, 9.967672664350237, 10.172747072226707, 10.348561454048813, 10.499358153814587, 10.628613920820545, 10.739180439446116, 10.83339557298905, 10.913172055455625, 10.980068438118069, 11.035345826610259, 11.080013066761827, 11.114862403954268, 11.140497164124545, 11.157352631809927, 11.165710998273518]]]

        phi_test = np.array(phi_test)

        # Test the scalar flux
        l = 0
        phi = pydgm.state.mg_phi[l, :, :].flatten()
        phi_zero_test = phi_test[:, l].flatten()
        np.testing.assert_array_almost_equal(phi, phi_zero_test, 7)

        self.angular_test()

    def test_solver_basic_2D_2g_1a_vacuum_eigen(self):
        '''
        Test for a basic 2 group problem
        '''
        self.set_eigen()
        self.set_mesh('simple')
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 0.0
        pydgm.control.boundary_south = 0.0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[0.2487746067595804, 0.30933535885463925, 0.36503957161582756, 0.4201277246266406, 0.4727429041064538, 0.5219789831678958, 0.5666972948641681, 0.6060354489662487, 0.6392379836284101, 0.6656917181028958, 0.6849238962362818, 0.6965974817500068, 0.7005110260557053, 0.6965974817500072, 0.6849238962362818, 0.6656917181028954, 0.6392379836284099, 0.6060354489662486, 0.5666972948641676, 0.5219789831678954, 0.47274290410645325, 0.4201277246266398, 0.3650395716158268, 0.30933535885463875, 0.24877460675958005, 0.3093353588546392, 0.40164987296136834, 0.48291526870614243, 0.5584914296565835, 0.6312485387266421, 0.6988077036867092, 0.7601167557294932, 0.813912097913677, 0.8592449558483541, 0.8953214292816684, 0.92152628635136, 0.9374235947881444, 0.9427517097445433, 0.9374235947881437, 0.9215262863513597, 0.8953214292816681, 0.8592449558483536, 0.8139120979136766, 0.7601167557294923, 0.698807703686708, 0.6312485387266414, 0.5584914296565827, 0.48291526870614165, 0.40164987296136784, 0.3093353588546388, 0.36503957161582756, 0.4829152687061422, 0.5944451912542015, 0.6940912164324666, 0.7860949620587045, 0.8723187135451134, 0.9500816973490145, 1.0183122596044265, 1.0757218667223183, 1.1213682123712332, 1.1545053937082992, 1.174599589924656, 1.1813330856367277, 1.1745995899246553, 1.1545053937082987, 1.121368212371233, 1.0757218667223176, 1.0183122596044252, 0.950081697349013, 0.8723187135451121, 0.7860949620587036, 0.694091216432466, 0.5944451912542007, 0.48291526870614176, 0.36503957161582723, 0.4201277246266406, 0.5584914296565837, 0.6940912164324667, 0.8215542114308743, 0.9352477382783926, 1.0386119631536603, 1.132791234434996, 1.2149670473854255, 1.284144202657454, 1.3390943477694461, 1.3789641487964708, 1.4031352581076166, 1.4112332698908574, 1.4031352581076166, 1.3789641487964701, 1.3390943477694455, 1.2841442026574532, 1.2149670473854237, 1.1327912344349942, 1.0386119631536588, 0.9352477382783915, 0.8215542114308731, 0.6940912164324659, 0.5584914296565832, 0.4201277246266401, 0.47274290410645387, 0.6312485387266424, 0.7860949620587048, 0.9352477382783928, 1.0736610472994341, 1.1957589812484655, 1.3044202797066318, 1.4002986998355933, 1.480566815593873, 1.5443844450713775, 1.590659651713007, 1.618703820457089, 1.6280998521423597, 1.6187038204570887, 1.5906596517130063, 1.5443844450713762, 1.4805668155938718, 1.400298699835592, 1.3044202797066304, 1.1957589812484641, 1.0736610472994326, 0.9352477382783914, 0.7860949620587037, 0.6312485387266413, 0.47274290410645303, 0.5219789831678961, 0.6988077036867091, 0.8723187135451133, 1.0386119631536603, 1.1957589812484652, 1.3391074138222738, 1.463235534944001, 1.5706511446747617, 1.661703820432259, 1.7336628995791248, 1.785911181959954, 1.8175629277589989, 1.8281624800473772, 1.8175629277589982, 1.7859111819599531, 1.7336628995791235, 1.6617038204322576, 1.5706511446747609, 1.463235534944001, 1.3391074138222734, 1.195758981248464, 1.0386119631536588, 0.872318713545112, 0.6988077036867077, 0.5219789831678953, 0.5666972948641688, 0.7601167557294939, 0.9500816973490143, 1.1327912344349955, 1.304420279706632, 1.4632355349440012, 1.6050104613189407, 1.7245450833554363, 1.8241342432960628, 1.9039815054710298, 1.9615421041215386, 1.9964802438076725, 2.0081817572886504, 1.9964802438076716, 1.9615421041215384, 1.9039815054710294, 1.8241342432960614, 1.724545083355435, 1.6050104613189402, 1.4632355349440005, 1.3044202797066307, 1.132791234434994, 0.9500816973490128, 0.760116755729492, 0.5666972948641678, 0.6060354489662493, 0.8139120979136776, 1.0183122596044265, 1.2149670473854246, 1.400298699835593, 1.5706511446747617, 1.724545083355436, 1.8581966015787008, 1.9666783752660877, 2.0522072216331457, 2.114975856603474, 2.152703108428814, 2.1653793244298796, 2.1527031084288137, 2.114975856603474, 2.0522072216331453, 1.9666783752660866, 1.8581966015786995, 1.7245450833554352, 1.570651144674761, 1.4002986998355924, 1.2149670473854235, 1.018312259604425, 0.8139120979136766, 0.6060354489662485, 0.6392379836284107, 0.859244955848355, 1.0757218667223187, 1.2841442026574539, 1.4805668155938723, 1.661703820432259, 1.8241342432960632, 1.9666783752660877, 2.0860050936007664, 2.1774982372953064, 2.243415389846528, 2.284049071070629, 2.297430887485442, 2.2840490710706294, 2.243415389846527, 2.1774982372953033, 2.086005093600764, 1.9666783752660864, 1.824134243296061, 1.6617038204322578, 1.4805668155938714, 1.2841442026574532, 1.0757218667223174, 0.8592449558483536, 0.6392379836284099, 0.6656917181028967, 0.8953214292816696, 1.1213682123712334, 1.3390943477694452, 1.5443844450713782, 1.7336628995791252, 1.9039815054710307, 2.0522072216331466, 2.177498237295307, 2.276984903871456, 2.3463849560806116, 2.3880835394753026, 2.402706436696479, 2.388083539475304, 2.3463849560806103, 2.276984903871452, 2.1774982372953047, 2.0522072216331444, 1.9039815054710287, 1.7336628995791237, 1.5443844450713762, 1.3390943477694448, 1.1213682123712327, 0.8953214292816684, 0.6656917181028957, 0.6849238962362824, 0.9215262863513608, 1.1545053937082996, 1.3789641487964708, 1.590659651713007, 1.7859111819599531, 1.9615421041215388, 2.1149758566034755, 2.2434153898465286, 2.3463849560806116, 2.4214652692362337, 2.4648625085214766, 2.4785988981976548, 2.464862508521476, 2.421465269236231, 2.34638495608061, 2.2434153898465263, 2.114975856603473, 1.9615421041215368, 1.7859111819599527, 1.590659651713006, 1.37896414879647, 1.1545053937082985, 0.9215262863513604, 0.684923896236282, 0.6965974817500075, 0.9374235947881446, 1.1745995899246564, 1.4031352581076177, 1.6187038204570894, 1.8175629277589984, 1.9964802438076719, 2.1527031084288146, 2.2840490710706303, 2.3880835394753044, 2.4648625085214766, 2.5118370812605506, 2.5268458313707605, 2.511837081260549, 2.4648625085214757, 2.3880835394753026, 2.2840490710706276, 2.152703108428813, 1.9964802438076716, 1.8175629277589982, 1.6187038204570894, 1.4031352581076162, 1.1745995899246557, 0.9374235947881441, 0.6965974817500072, 0.7005110260557053, 0.9427517097445437, 1.1813330856367281, 1.411233269890858, 1.6280998521423609, 1.8281624800473772, 2.008181757288651, 2.16537932442988, 2.2974308874854423, 2.4027064366964797, 2.478598898197655, 2.526845831370762, 2.544995566124512, 2.526845831370761, 2.478598898197654, 2.4027064366964774, 2.29743088748544, 2.1653793244298787, 2.008181757288651, 1.828162480047377, 1.6280998521423604, 1.4112332698908572, 1.1813330856367281, 0.942751709744544, 0.7005110260557053, 0.696597481750007, 0.9374235947881437, 1.1745995899246553, 1.4031352581076164, 1.6187038204570892, 1.817562927758998, 1.9964802438076719, 2.152703108428814, 2.284049071070629, 2.3880835394753035, 2.4648625085214775, 2.5118370812605497, 2.526845831370762, 2.511837081260549, 2.4648625085214744, 2.388083539475302, 2.284049071070627, 2.1527031084288137, 1.9964802438076714, 1.8175629277589977, 1.6187038204570898, 1.403135258107617, 1.1745995899246562, 0.9374235947881443, 0.6965974817500074, 0.6849238962362815, 0.9215262863513597, 1.1545053937082983, 1.37896414879647, 1.5906596517130056, 1.785911181959953, 1.9615421041215382, 2.1149758566034746, 2.2434153898465277, 2.346384956080611, 2.4214652692362324, 2.464862508521476, 2.478598898197654, 2.464862508521475, 2.4214652692362306, 2.34638495608061, 2.2434153898465268, 2.114975856603473, 1.9615421041215373, 1.7859111819599534, 1.5906596517130067, 1.3789641487964701, 1.154505393708299, 0.9215262863513605, 0.6849238962362822, 0.6656917181028956, 0.8953214292816684, 1.1213682123712325, 1.3390943477694441, 1.5443844450713762, 1.7336628995791235, 1.9039815054710296, 2.0522072216331453, 2.177498237295306, 2.2769849038714542, 2.3463849560806107, 2.388083539475303, 2.4027064366964783, 2.3880835394753013, 2.3463849560806094, 2.2769849038714542, 2.1774982372953042, 2.0522072216331435, 1.903981505471029, 1.733662899579124, 1.5443844450713766, 1.3390943477694452, 1.1213682123712334, 0.8953214292816688, 0.6656917181028961, 0.6392379836284101, 0.8592449558483539, 1.0757218667223172, 1.2841442026574528, 1.4805668155938716, 1.6617038204322572, 1.824134243296061, 1.966678375266086, 2.0860050936007646, 2.177498237295305, 2.243415389846527, 2.2840490710706276, 2.2974308874854406, 2.2840490710706276, 2.2434153898465268, 2.1774982372953056, 2.0860050936007637, 1.966678375266086, 1.8241342432960603, 1.6617038204322567, 1.4805668155938712, 1.2841442026574534, 1.0757218667223183, 0.8592449558483548, 0.6392379836284101, 0.6060354489662485, 0.8139120979136767, 1.0183122596044252, 1.214967047385424, 1.4002986998355924, 1.5706511446747604, 1.724545083355434, 1.8581966015786986, 1.966678375266085, 2.052207221633143, 2.114975856603472, 2.1527031084288124, 2.165379324429878, 2.152703108428813, 2.1149758566034733, 2.0522072216331444, 1.9666783752660861, 1.8581966015786993, 1.7245450833554339, 1.5706511446747597, 1.400298699835592, 1.2149670473854246, 1.018312259604426, 0.8139120979136778, 0.6060354489662493, 0.5666972948641678, 0.7601167557294926, 0.9500816973490129, 1.132791234434994, 1.3044202797066307, 1.4632355349439998, 1.6050104613189393, 1.7245450833554337, 1.8241342432960592, 1.9039815054710265, 1.9615421041215355, 1.99648024380767, 2.0081817572886496, 1.9964802438076705, 1.9615421041215368, 1.9039815054710283, 1.8241342432960603, 1.724545083355434, 1.6050104613189389, 1.4632355349439996, 1.3044202797066304, 1.1327912344349949, 0.9500816973490139, 0.7601167557294932, 0.5666972948641683, 0.5219789831678955, 0.6988077036867083, 0.8723187135451121, 1.0386119631536588, 1.1957589812484641, 1.3391074138222725, 1.4632355349439998, 1.5706511446747595, 1.6617038204322556, 1.733662899579122, 1.7859111819599514, 1.8175629277589964, 1.828162480047376, 1.8175629277589962, 1.785911181959952, 1.7336628995791221, 1.6617038204322565, 1.5706511446747602, 1.4632355349439996, 1.3391074138222723, 1.195758981248464, 1.0386119631536592, 0.8723187135451124, 0.6988077036867084, 0.5219789831678958, 0.47274290410645325, 0.6312485387266413, 0.7860949620587037, 0.9352477382783914, 1.0736610472994323, 1.1957589812484632, 1.3044202797066298, 1.4002986998355915, 1.4805668155938698, 1.5443844450713744, 1.5906596517130036, 1.618703820457087, 1.628099852142358, 1.6187038204570874, 1.5906596517130043, 1.5443844450713748, 1.48056681559387, 1.400298699835591, 1.3044202797066302, 1.1957589812484637, 1.0736610472994326, 0.9352477382783915, 0.7860949620587039, 0.6312485387266413, 0.4727429041064536, 0.42012772462664005, 0.558491429656583, 0.6940912164324656, 0.821554211430873, 0.9352477382783911, 1.0386119631536583, 1.1327912344349942, 1.214967047385423, 1.2841442026574517, 1.3390943477694435, 1.3789641487964681, 1.4031352581076144, 1.411233269890855, 1.4031352581076149, 1.378964148796469, 1.3390943477694435, 1.2841442026574519, 1.214967047385423, 1.1327912344349942, 1.0386119631536583, 0.9352477382783914, 0.8215542114308733, 0.6940912164324659, 0.5584914296565829, 0.4201277246266399, 0.3650395716158271, 0.4829152687061416, 0.5944451912542004, 0.6940912164324654, 0.7860949620587033, 0.872318713545112, 0.950081697349013, 1.0183122596044247, 1.0757218667223167, 1.1213682123712319, 1.1545053937082967, 1.1745995899246537, 1.181333085636726, 1.1745995899246535, 1.1545053937082974, 1.1213682123712316, 1.0757218667223165, 1.0183122596044245, 0.9500816973490126, 0.8723187135451116, 0.7860949620587037, 0.6940912164324659, 0.5944451912542006, 0.4829152687061415, 0.36503957161582695, 0.3093353588546387, 0.4016498729613677, 0.4829152687061415, 0.5584914296565826, 0.6312485387266412, 0.6988077036867079, 0.7601167557294921, 0.8139120979136765, 0.8592449558483536, 0.8953214292816674, 0.9215262863513591, 0.9374235947881425, 0.9427517097445415, 0.9374235947881424, 0.9215262863513588, 0.8953214292816672, 0.8592449558483534, 0.8139120979136764, 0.760116755729492, 0.6988077036867076, 0.6312485387266412, 0.5584914296565827, 0.4829152687061414, 0.4016498729613678, 0.3093353588546387, 0.24877460675957994, 0.3093353588546386, 0.36503957161582684, 0.42012772462663983, 0.47274290410645287, 0.5219789831678951, 0.5666972948641678, 0.6060354489662485, 0.6392379836284093, 0.6656917181028953, 0.6849238962362811, 0.6965974817500061, 0.7005110260557043, 0.6965974817500061, 0.684923896236281, 0.6656917181028952, 0.6392379836284097, 0.606035448966248, 0.5666972948641674, 0.5219789831678951, 0.47274290410645314, 0.42012772462663994, 0.3650395716158269, 0.3093353588546386, 0.24877460675958013]], [[0.01998505220506663, 0.028624451099833366, 0.03645151076496133, 0.04399260475136248, 0.05100072704478553, 0.05739396487095979, 0.06307779967625268, 0.067997245315577, 0.07209514838534635, 0.07532933795436803, 0.0776647807484596, 0.07907628103283944, 0.07954850885838675, 0.07907628103283944, 0.07766478074845957, 0.075329337954368, 0.07209514838534632, 0.06799724531557698, 0.06307779967625264, 0.057393964870959754, 0.05100072704478547, 0.043992604751362394, 0.036451510764961274, 0.028624451099833345, 0.019985052205066602, 0.028624451099833387, 0.04289219826344366, 0.05537627658493564, 0.06683400942917612, 0.07756460151772676, 0.08729947508349442, 0.09596646083873438, 0.10345581477898921, 0.10969794646838663, 0.11462311713123982, 0.1181799334309722, 0.12032968475616068, 0.12104887790598191, 0.12032968475616067, 0.1181799334309722, 0.11462311713123977, 0.1096979464683866, 0.10345581477898919, 0.09596646083873432, 0.08729947508349438, 0.07756460151772669, 0.06683400942917608, 0.055376276584935595, 0.04289219826344358, 0.02862445109983335, 0.036451510764961344, 0.05537627658493567, 0.07281240864873842, 0.08833946431758972, 0.10251035073030715, 0.11547966534412975, 0.12697133089098303, 0.13691796221646127, 0.1451970438988955, 0.1517319977604755, 0.1564501107528323, 0.15930170090015233, 0.16025573986215147, 0.15930170090015233, 0.15645011075283227, 0.1517319977604754, 0.1451970438988954, 0.13691796221646116, 0.126971330890983, 0.11547966534412962, 0.10251035073030706, 0.08833946431758967, 0.07281240864873835, 0.0553762765849356, 0.03645151076496128, 0.04399260475136246, 0.06683400942917615, 0.08833946431758974, 0.10812515410923546, 0.12576424655216117, 0.14166281810818404, 0.15587030482414796, 0.16810882465046229, 0.17831532245918838, 0.18636112398825838, 0.19217229897749483, 0.19568374851974488, 0.1968584242752685, 0.19568374851974477, 0.1921722989774947, 0.1863611239882583, 0.1783153224591883, 0.16810882465046217, 0.15587030482414788, 0.1416628181081839, 0.12576424655216112, 0.10812515410923533, 0.08833946431758966, 0.06683400942917607, 0.04399260475136238, 0.05100072704478551, 0.07756460151772678, 0.10251035073030718, 0.1257642465521612, 0.14699529578237652, 0.16577082703609106, 0.18238584389256482, 0.19681538872095647, 0.20878732915049025, 0.2182473780344291, 0.225070203331361, 0.22919492827762505, 0.23057461282062075, 0.22919492827762494, 0.22507020333136094, 0.21824737803442895, 0.20878732915049006, 0.19681538872095633, 0.18238584389256474, 0.16577082703609097, 0.14699529578237644, 0.1257642465521611, 0.10251035073030706, 0.07756460151772662, 0.05100072704478543, 0.057393964870959775, 0.08729947508349441, 0.11547966534412972, 0.14166281810818399, 0.16577082703609108, 0.18750266335421473, 0.20642199389721985, 0.22274385294262125, 0.23639580825188378, 0.24712057785504718, 0.2548797983308887, 0.2595620678850089, 0.26112952299654413, 0.25956206788500885, 0.25487979833088864, 0.24712057785504704, 0.23639580825188358, 0.22274385294262108, 0.20642199389721977, 0.1875026633542146, 0.16577082703609095, 0.14166281810818385, 0.11547966534412953, 0.08729947508349425, 0.05739396487095971, 0.06307779967625268, 0.0959664608387344, 0.126971330890983, 0.15587030482414793, 0.1823858438925648, 0.2064219938972199, 0.22769822236798304, 0.24578147642763298, 0.2608347764396368, 0.2727617209937381, 0.28132937120877516, 0.28652333758737614, 0.2882555932407505, 0.28652333758737614, 0.28132937120877494, 0.2727617209937379, 0.2608347764396366, 0.24578147642763265, 0.22769822236798287, 0.2064219938972197, 0.18238584389256465, 0.1558703048241477, 0.1269713308909828, 0.09596646083873425, 0.0630777996762526, 0.06799724531557702, 0.10345581477898926, 0.13691796221646121, 0.16810882465046226, 0.19681538872095627, 0.22274385294262114, 0.24578147642763293, 0.26566827591237996, 0.28198376832678235, 0.2948636707750291, 0.3042076650579847, 0.30981520997629597, 0.3117071758004514, 0.3098152099762959, 0.3042076650579845, 0.29486367077502895, 0.2819837683267821, 0.26566827591237957, 0.24578147642763262, 0.22274385294262097, 0.1968153887209561, 0.16810882465046204, 0.13691796221646108, 0.10345581477898912, 0.06799724531557694, 0.07209514838534634, 0.10969794646838667, 0.14519704389889548, 0.1783153224591884, 0.20878732915049014, 0.23639580825188367, 0.2608347764396368, 0.2819837683267825, 0.29960847209767005, 0.31331052795118874, 0.32321880946406617, 0.3292494667036456, 0.33122850555567945, 0.3292494667036456, 0.323218809464066, 0.31331052795118847, 0.29960847209766955, 0.28198376832678207, 0.2608347764396365, 0.2363958082518834, 0.20878732915049, 0.17831532245918816, 0.14519704389889518, 0.10969794646838649, 0.07209514838534624, 0.07532933795436803, 0.11462311713123982, 0.15173199776047552, 0.1863611239882584, 0.2182473780344291, 0.24712057785504715, 0.27276172099373797, 0.29486367077502923, 0.31331052795118886, 0.3278999450140935, 0.3382680210151431, 0.3445408145247518, 0.3466961419642437, 0.34454081452475166, 0.33826802101514275, 0.327899945014093, 0.3133105279511884, 0.29486367077502884, 0.2727617209937377, 0.2471205778550469, 0.21824737803442884, 0.18636112398825816, 0.15173199776047527, 0.11462311713123965, 0.07532933795436791, 0.07766478074845957, 0.11817993343097222, 0.1564501107528323, 0.19217229897749483, 0.22507020333136107, 0.25487979833088875, 0.28132937120877516, 0.3042076650579848, 0.32321880946406634, 0.3382680210151432, 0.3491782796062605, 0.3556589542210299, 0.357796817251322, 0.3556589542210296, 0.34917827960626024, 0.33826802101514264, 0.32321880946406584, 0.3042076650579843, 0.2813293712087748, 0.2548797983308885, 0.22507020333136074, 0.19217229897749455, 0.15645011075283208, 0.11817993343097205, 0.07766478074845946, 0.07907628103283938, 0.12032968475616064, 0.15930170090015233, 0.1956837485197449, 0.22919492827762514, 0.2595620678850089, 0.2865233375873762, 0.3098152099762961, 0.32924946670364585, 0.344540814524752, 0.35565895422102983, 0.36240803074961725, 0.36459041779744544, 0.36240803074961697, 0.35565895422102956, 0.3445408145247515, 0.3292494667036454, 0.30981520997629564, 0.2865233375873758, 0.2595620678850086, 0.2291949282776248, 0.19568374851974465, 0.1593017009001521, 0.12032968475616053, 0.07907628103283933, 0.0795485088583867, 0.12104887790598186, 0.16025573986215144, 0.19685842427526862, 0.23057461282062083, 0.2611295229965441, 0.2882555932407507, 0.3117071758004516, 0.3312285055556798, 0.3466961419642438, 0.3577968172513219, 0.36459041779744533, 0.36700813351718253, 0.3645904177974454, 0.3577968172513218, 0.3466961419642433, 0.3312285055556792, 0.31170717580045104, 0.28825559324075023, 0.2611295229965439, 0.23057461282062056, 0.19685842427526837, 0.16025573986215128, 0.12104887790598169, 0.07954850885838664, 0.07907628103283937, 0.1203296847561606, 0.15930170090015222, 0.19568374851974482, 0.229194928277625, 0.2595620678850089, 0.28652333758737614, 0.30981520997629614, 0.3292494667036457, 0.34454081452475166, 0.3556589542210297, 0.3624080307496171, 0.3645904177974454, 0.3624080307496171, 0.3556589542210296, 0.34454081452475144, 0.3292494667036452, 0.3098152099762958, 0.2865233375873758, 0.25956206788500863, 0.22919492827762492, 0.19568374851974468, 0.15930170090015214, 0.12032968475616056, 0.0790762810328393, 0.07766478074845959, 0.11817993343097216, 0.15645011075283216, 0.19217229897749472, 0.2250702033313609, 0.2548797983308887, 0.2813293712087751, 0.30420766505798474, 0.32321880946406617, 0.33826802101514303, 0.34917827960626036, 0.3556589542210297, 0.35779681725132184, 0.35565895422102967, 0.3491782796062603, 0.3382680210151428, 0.3232188094640659, 0.3042076650579844, 0.2813293712087748, 0.2548797983308885, 0.22507020333136085, 0.1921722989774947, 0.1564501107528321, 0.11817993343097208, 0.07766478074845945, 0.075329337954368, 0.11462311713123972, 0.15173199776047533, 0.18636112398825833, 0.2182473780344291, 0.2471205778550471, 0.2727617209937379, 0.2948636707750291, 0.3133105279511887, 0.3278999450140934, 0.33826802101514303, 0.34454081452475155, 0.34669614196424364, 0.3445408145247516, 0.33826802101514286, 0.32789994501409314, 0.3133105279511885, 0.2948636707750289, 0.2727617209937377, 0.24712057785504687, 0.21824737803442884, 0.18636112398825821, 0.15173199776047533, 0.11462311713123967, 0.07532933795436793, 0.0720951483853463, 0.10969794646838658, 0.14519704389889537, 0.17831532245918832, 0.20878732915049014, 0.2363958082518836, 0.2608347764396367, 0.28198376832678224, 0.29960847209766983, 0.3133105279511886, 0.32321880946406595, 0.3292494667036455, 0.3312285055556795, 0.32924946670364563, 0.32321880946406606, 0.3133105279511885, 0.2996084720976697, 0.28198376832678207, 0.2608347764396365, 0.2363958082518834, 0.20878732915049, 0.17831532245918827, 0.14519704389889534, 0.10969794646838664, 0.07209514838534628, 0.06799724531557692, 0.10345581477898914, 0.13691796221646116, 0.1681088246504622, 0.1968153887209563, 0.22274385294262114, 0.24578147642763282, 0.26566827591237974, 0.28198376832678224, 0.294863670775029, 0.30420766505798447, 0.30981520997629586, 0.3117071758004514, 0.309815209976296, 0.3042076650579846, 0.29486367077502895, 0.28198376832678207, 0.26566827591237946, 0.24578147642763268, 0.22274385294262103, 0.1968153887209562, 0.16810882465046217, 0.1369179622164611, 0.10345581477898914, 0.06799724531557695, 0.06307779967625264, 0.09596646083873434, 0.12697133089098292, 0.15587030482414788, 0.18238584389256474, 0.2064219938972198, 0.22769822236798282, 0.24578147642763276, 0.2608347764396366, 0.2727617209937378, 0.28132937120877494, 0.2865233375873759, 0.2882555932407505, 0.28652333758737614, 0.28132937120877494, 0.2727617209937377, 0.26083477643963643, 0.2457814764276326, 0.22769822236798273, 0.20642199389721966, 0.18238584389256474, 0.1558703048241478, 0.12697133089098286, 0.0959664608387343, 0.06307779967625263, 0.057393964870959734, 0.08729947508349435, 0.1154796653441296, 0.1416628181081839, 0.165770827036091, 0.1875026633542146, 0.20642199389721977, 0.22274385294262092, 0.23639580825188347, 0.24712057785504693, 0.25487979833088853, 0.25956206788500874, 0.2611295229965441, 0.2595620678850088, 0.25487979833088864, 0.24712057785504699, 0.2363958082518835, 0.22274385294262092, 0.2064219938972196, 0.18750266335421453, 0.16577082703609092, 0.14166281810818385, 0.11547966534412955, 0.08729947508349435, 0.05739396487095975, 0.05100072704478549, 0.07756460151772669, 0.10251035073030709, 0.12576424655216104, 0.14699529578237644, 0.16577082703609092, 0.18238584389256463, 0.19681538872095608, 0.20878732915048992, 0.2182473780344288, 0.22507020333136082, 0.22919492827762483, 0.23057461282062058, 0.2291949282776249, 0.22507020333136082, 0.21824737803442895, 0.20878732915049003, 0.19681538872095614, 0.18238584389256465, 0.16577082703609092, 0.14699529578237638, 0.125764246552161, 0.10251035073030706, 0.07756460151772666, 0.05100072704478548, 0.04399260475136242, 0.06683400942917608, 0.08833946431758964, 0.10812515410923533, 0.12576424655216106, 0.1416628181081838, 0.15587030482414774, 0.16810882465046206, 0.1783153224591881, 0.18636112398825808, 0.19217229897749458, 0.19568374851974465, 0.19685842427526834, 0.19568374851974465, 0.19217229897749458, 0.1863611239882582, 0.17831532245918824, 0.1681088246504621, 0.1558703048241478, 0.14166281810818382, 0.12576424655216106, 0.10812515410923529, 0.08833946431758967, 0.06683400942917608, 0.043992604751362414, 0.03645151076496128, 0.055376276584935595, 0.07281240864873831, 0.0883394643175896, 0.102510350730307, 0.11547966534412953, 0.12697133089098286, 0.13691796221646105, 0.14519704389889526, 0.15173199776047522, 0.15645011075283208, 0.1593017009001521, 0.16025573986215125, 0.1593017009001521, 0.1564501107528321, 0.15173199776047538, 0.14519704389889532, 0.1369179622164611, 0.12697133089098284, 0.11547966534412958, 0.10251035073030708, 0.08833946431758967, 0.07281240864873834, 0.055376276584935574, 0.036451510764961274, 0.028624451099833324, 0.04289219826344357, 0.055376276584935574, 0.06683400942917601, 0.07756460151772661, 0.08729947508349428, 0.09596646083873418, 0.10345581477898907, 0.10969794646838647, 0.11462311713123963, 0.11817993343097204, 0.12032968475616049, 0.12104887790598168, 0.12032968475616052, 0.11817993343097209, 0.11462311713123971, 0.10969794646838653, 0.10345581477898909, 0.09596646083873425, 0.0872994750834943, 0.07756460151772665, 0.06683400942917607, 0.0553762765849356, 0.04289219826344358, 0.028624451099833324, 0.01998505220506658, 0.028624451099833328, 0.03645151076496123, 0.04399260475136236, 0.05100072704478543, 0.05739396487095966, 0.06307779967625257, 0.06799724531557688, 0.07209514838534621, 0.07532933795436791, 0.07766478074845945, 0.07907628103283927, 0.07954850885838662, 0.07907628103283931, 0.07766478074845949, 0.0753293379543679, 0.07209514838534624, 0.0679972453155769, 0.06307779967625259, 0.05739396487095971, 0.05100072704478544, 0.0439926047513624, 0.036451510764961274, 0.028624451099833328, 0.019985052205066585]]]

        phi_test = np.array(phi_test)

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, 0.23385815, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 7)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l0_simple(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        self.set_eigen()
        self.set_mesh('slab')
        pydgm.control.scatter_leg_order = 0
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[2.0222116180374377, 3.906659286632303, 5.489546165510137, 6.624935332662817, 7.217123379989135, 7.217123379989135, 6.624935332662812, 5.4895461655101325, 3.9066592866322987, 2.022211618037434, 2.0222116180374723, 3.906659286632373, 5.489546165510238, 6.624935332662936, 7.217123379989267, 7.217123379989266, 6.624935332662933, 5.489546165510232, 3.906659286632369, 2.02221161803747, 2.0222116180375425, 3.906659286632511, 5.4895461655104345, 6.624935332663176, 7.2171233799895305, 7.217123379989527, 6.624935332663175, 5.489546165510432, 3.9066592866325083, 2.02221161803754, 2.0222116180376455, 3.9066592866327152, 5.489546165510723, 6.6249353326635285, 7.217123379989911, 7.21712337998991, 6.624935332663527, 5.48954616551072, 3.9066592866327117, 2.022211618037643, 2.022211618037778, 3.9066592866329786, 5.489546165511096, 6.62493533266398, 7.217123379990407, 7.217123379990406, 6.624935332663978, 5.489546165511094, 3.906659286632976, 2.022211618037777, 2.022211618037936, 3.906659286633293, 5.489546165511546, 6.624935332664524, 7.217123379991003, 7.217123379991001, 6.62493533266452, 5.489546165511541, 3.9066592866332917, 2.022211618037936, 2.02221161803812, 3.9066592866336483, 5.489546165512049, 6.624935332665141, 7.217123379991674, 7.217123379991672, 6.624935332665138, 5.489546165512053, 3.906659286633648, 2.0222116180381193, 2.02221161803832, 3.9066592866340404, 5.489546165512603, 6.624935332665814, 7.217123379992408, 7.217123379992409, 6.6249353326658165, 5.489546165512604, 3.906659286634039, 2.0222116180383196, 2.0222116180385177, 3.9066592866344605, 5.489546165513193, 6.624935332666522, 7.217123379993187, 7.217123379993187, 6.624935332666523, 5.489546165513196, 3.9066592866344605, 2.022211618038519, 2.0222116180387206, 3.9066592866348797, 5.489546165513811, 6.624935332667246, 7.217123379993982, 7.217123379993986, 6.624935332667246, 5.48954616551381, 3.9066592866348824, 2.0222116180387224, 2.0222116180389453, 3.906659286635285, 5.489546165514407, 6.6249353326679925, 7.217123379994771, 7.217123379994772, 6.624935332667999, 5.48954616551441, 3.906659286635288, 2.022211618038948, 2.0222116180391927, 3.906659286635688, 5.48954616551496, 6.624935332668722, 7.217123379995537, 7.217123379995538, 6.624935332668729, 5.489546165514966, 3.9066592866356924, 2.0222116180391954, 2.022211618039421, 3.906659286636115, 5.489546165515496, 6.624935332669343, 7.217123379996293, 7.217123379996299, 6.624935332669352, 5.489546165515503, 3.906659286636122, 2.022211618039423, 2.02221161803949, 3.9066592866365792, 5.489546165516017, 6.62493533266986, 7.217123379997003, 7.217123379997005, 6.624935332669865, 5.489546165516022, 3.9066592866365855, 2.0222116180394942, 2.0222116180396172, 3.9066592866368017, 5.489546165516571, 6.624935332670406, 7.217123379997539, 7.217123379997541, 6.624935332670408, 5.489546165516575, 3.9066592866368084, 2.022211618039622, 2.0222116180400502, 3.9066592866368364, 5.489546165516934, 6.624935332671166, 7.217123379997814, 7.217123379997816, 6.62493533267117, 5.489546165516938, 3.9066592866368413, 2.0222116180400542, 2.0222116180400302, 3.9066592866373284, 5.489546165517048, 6.624935332671695, 7.217123379998117, 7.217123379998122, 6.624935332671701, 5.489546165517053, 3.9066592866373346, 2.022211618040033, 2.0222116180394636, 3.9066592866377623, 5.4895461655177265, 6.624935332671153, 7.217123379998839, 7.217123379998841, 6.624935332671155, 5.489546165517731, 3.9066592866377667, 2.022211618039466, 2.022211618039759, 3.9066592866374505, 5.489546165518068, 6.624935332670921, 7.217123379999226, 7.217123379999228, 6.624935332670927, 5.489546165518074, 3.906659286637456, 2.0222116180397633, 2.0222116180410867, 3.9066592866369314, 5.489546165516315, 6.624935332671973, 7.217123379998163, 7.217123379998167, 6.6249353326719795, 5.489546165516322, 3.9066592866369385, 2.0222116180410916]], [[0.2601203722850905, 0.5582585327512433, 0.7906322218586104, 0.9549760069773039, 1.040451416793767, 1.0404514167937677, 0.9549760069773037, 0.7906322218586092, 0.5582585327512429, 0.26012037228509016, 0.260120372285095, 0.5582585327512531, 0.7906322218586241, 0.9549760069773205, 1.040451416793786, 1.0404514167937855, 0.9549760069773202, 0.7906322218586236, 0.5582585327512527, 0.2601203722850945, 0.260120372285104, 0.5582585327512725, 0.7906322218586517, 0.9549760069773544, 1.0404514167938226, 1.0404514167938221, 0.9549760069773543, 0.7906322218586515, 0.558258532751272, 0.2601203722851037, 0.26012037228511703, 0.5582585327513011, 0.7906322218586924, 0.9549760069774041, 1.040451416793876, 1.0404514167938763, 0.9549760069774037, 0.7906322218586922, 0.5582585327513006, 0.26012037228511686, 0.26012037228513407, 0.5582585327513375, 0.7906322218587449, 0.954976006977468, 1.040451416793946, 1.040451416793946, 0.9549760069774672, 0.7906322218587444, 0.5582585327513372, 0.26012037228513396, 0.26012037228515444, 0.5582585327513817, 0.7906322218588078, 0.954976006977544, 1.0404514167940295, 1.040451416794029, 0.9549760069775434, 0.7906322218588072, 0.5582585327513814, 0.2601203722851543, 0.2601203722851778, 0.5582585327514316, 0.790632221858879, 0.9549760069776305, 1.0404514167941241, 1.040451416794124, 0.9549760069776303, 0.7906322218588783, 0.5582585327514313, 0.26012037228517765, 0.26012037228520346, 0.558258532751486, 0.7906322218589572, 0.9549760069777256, 1.0404514167942274, 1.0404514167942271, 0.9549760069777252, 0.7906322218589572, 0.5582585327514857, 0.26012037228520346, 0.2601203722852295, 0.5582585327515446, 0.7906322218590393, 0.9549760069778253, 1.0404514167943364, 1.0404514167943366, 0.9549760069778253, 0.7906322218590391, 0.5582585327515445, 0.2601203722852295, 0.26012037228525536, 0.5582585327516034, 0.790632221859125, 0.9549760069779274, 1.0404514167944487, 1.0404514167944485, 0.9549760069779275, 0.7906322218591252, 0.5582585327516035, 0.26012037228525536, 0.2601203722852845, 0.5582585327516609, 0.7906322218592101, 0.9549760069780301, 1.0404514167945595, 1.0404514167945598, 0.9549760069780304, 0.7906322218592103, 0.5582585327516612, 0.2601203722852847, 0.26012037228531204, 0.5582585327517199, 0.7906322218592873, 0.9549760069781328, 1.0404514167946664, 1.0404514167946664, 0.9549760069781337, 0.7906322218592882, 0.5582585327517203, 0.26012037228531243, 0.2601203722853439, 0.5582585327517724, 0.7906322218593651, 0.9549760069782204, 1.0404514167947703, 1.0404514167947703, 0.9549760069782209, 0.7906322218593661, 0.5582585327517732, 0.2601203722853444, 0.26012037228535895, 0.5582585327518332, 0.7906322218594308, 0.954976006978293, 1.0404514167948657, 1.0404514167948657, 0.954976006978294, 0.7906322218594317, 0.5582585327518342, 0.26012037228535934, 0.26012037228535956, 0.5582585327518739, 0.7906322218594933, 0.9549760069783544, 1.0404514167949381, 1.0404514167949384, 0.954976006978355, 0.7906322218594941, 0.5582585327518749, 0.26012037228535995, 0.2601203722854187, 0.5582585327518456, 0.7906322218595377, 0.9549760069784322, 1.0404514167949561, 1.0404514167949563, 0.9549760069784329, 0.7906322218595386, 0.5582585327518462, 0.2601203722854192, 0.26012037228539797, 0.5582585327518799, 0.790632221859497, 0.9549760069785007, 1.0404514167949224, 1.040451416794923, 0.9549760069785015, 0.790632221859498, 0.5582585327518805, 0.2601203722853983, 0.26012037228518786, 0.5582585327519209, 0.7906322218595863, 0.9549760069782882, 1.0404514167949557, 1.040451416794956, 0.9549760069782894, 0.7906322218595871, 0.5582585327519218, 0.2601203722851882, 0.2601203722851841, 0.5582585327518561, 0.7906322218597195, 0.954976006978139, 1.0404514167950512, 1.0404514167950507, 0.9549760069781394, 0.7906322218597205, 0.5582585327518564, 0.26012037228518436, 0.2601203722858843, 0.5582585327521365, 0.7906322218596814, 0.9549760069791707, 1.0404514167954841, 1.0404514167954846, 0.9549760069791717, 0.7906322218596826, 0.5582585327521374, 0.2601203722858849]]]

        phi_test = np.array(phi_test)

        keff_test = 0.88662575

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l1_simple(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        self.set_eigen()
        self.set_mesh('slab')
        pydgm.control.scatter_leg_order = 1
        pydgm.control.angle_order = 8
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[2.2498290322633907, 3.8099808165357714, 4.9650347433443445, 5.816050082302227, 6.247855065193104, 6.247855065193103, 5.816050082302226, 4.965034743344341, 3.809980816535769, 2.2498290322633863, 2.2498290322629817, 3.8099808165350675, 4.965034743343417, 5.816050082301139, 6.247855065191926, 6.247855065191929, 5.8160500823011345, 4.965034743343412, 3.8099808165350653, 2.2498290322629773, 2.2498290322621717, 3.809980816533684, 4.965034743341592, 5.816050082298984, 6.247855065189607, 6.247855065189609, 5.816050082298982, 4.965034743341587, 3.8099808165336806, 2.2498290322621686, 2.2498290322609846, 3.80998081653165, 4.965034743338905, 5.816050082295824, 6.247855065186202, 6.247855065186203, 5.81605008229582, 4.965034743338904, 3.8099808165316476, 2.2498290322609806, 2.2498290322594463, 3.809980816529016, 4.96503474333543, 5.816050082291732, 6.247855065181794, 6.247855065181794, 5.816050082291735, 4.965034743335429, 3.8099808165290145, 2.2498290322594428, 2.249829032257595, 3.8099808165258495, 4.9650347433312545, 5.816050082286811, 6.247855065176496, 6.247855065176496, 5.816050082286813, 4.965034743331256, 3.8099808165258486, 2.249829032257593, 2.2498290322554784, 3.809980816522229, 4.965034743326478, 5.816050082281188, 6.2478550651704365, 6.247855065170436, 5.816050082281184, 4.96503474332648, 3.809980816522229, 2.2498290322554766, 2.2498290322531465, 3.80998081651824, 4.965034743321218, 5.816050082274992, 6.247855065163772, 6.24785506516377, 5.816050082274991, 4.965034743321221, 3.809980816518242, 2.249829032253145, 2.249829032250655, 3.8099808165139857, 4.965034743315607, 5.8160500822683865, 6.247855065156656, 6.247855065156653, 5.816050082268391, 4.965034743315609, 3.809980816513986, 2.249829032250656, 2.249829032248066, 3.8099808165095634, 4.965034743309781, 5.81605008226152, 6.247855065149262, 6.247855065149267, 5.816050082261525, 4.9650347433097854, 3.809980816509568, 2.249829032248068, 2.249829032245445, 3.809980816505085, 4.965034743303881, 5.816050082254577, 6.247855065141787, 6.247855065141788, 5.816050082254579, 4.965034743303885, 3.809980816505088, 2.249829032245447, 2.2498290322428507, 3.8099808165006572, 4.965034743298048, 5.816050082247715, 6.247855065134397, 6.2478550651344, 5.816050082247721, 4.965034743298054, 3.8099808165006612, 2.2498290322428534, 2.2498290322403496, 3.809980816496391, 4.965034743292428, 5.8160500822411025, 6.24785506512728, 6.2478550651272835, 5.816050082241108, 4.965034743292433, 3.809980816496396, 2.249829032240353, 2.249829032238001, 3.809980816492384, 4.965034743287158, 5.81605008223491, 6.247855065120606, 6.247855065120609, 5.8160500822349155, 4.9650347432871635, 3.809980816492392, 2.2498290322380057, 2.249829032235849, 3.8099808164887285, 4.965034743282348, 5.816050082229249, 6.247855065114524, 6.247855065114525, 5.816050082229254, 4.965034743282357, 3.8099808164887374, 2.249829032235856, 2.249829032233936, 3.809980816485456, 4.965034743278053, 5.816050082224198, 6.247855065109097, 6.2478550651091, 5.816050082224204, 4.965034743278061, 3.809980816485463, 2.249829032233942, 2.2498290322322183, 3.809980816482534, 4.965034743274238, 5.816050082219713, 6.247855065104247, 6.247855065104249, 5.8160500822197205, 4.965034743274245, 3.809980816482541, 2.2498290322322245, 2.2498290322306653, 3.809980816479877, 4.965034743270718, 5.816050082215531, 6.247855065099724, 6.247855065099732, 5.816050082215538, 4.965034743270726, 3.809980816479887, 2.2498290322306715, 2.249829032229158, 3.8099808164771685, 4.965034743267044, 5.816050082211081, 6.247855065094892, 6.247855065094892, 5.816050082211093, 4.965034743267053, 3.809980816477177, 2.2498290322291634, 2.2498290322278685, 3.8099808164752096, 4.965034743264343, 5.816050082207746, 6.247855065091241, 6.247855065091243, 5.816050082207756, 4.965034743264354, 3.809980816475222, 2.2498290322278756]], [[0.2799265605145948, 0.5275670222353585, 0.7003785331258843, 0.8245121493339169, 0.8859814447871472, 0.8859814447871469, 0.8245121493339159, 0.7003785331258839, 0.5275670222353577, 0.27992656051459425, 0.2799265605145487, 0.52756702223527, 0.7003785331257675, 0.8245121493337771, 0.8859814447869971, 0.8859814447869966, 0.824512149333777, 0.7003785331257665, 0.5275670222352696, 0.27992656051454823, 0.2799265605144572, 0.5275670222350973, 0.7003785331255358, 0.8245121493335024, 0.8859814447867008, 0.8859814447866997, 0.824512149333502, 0.7003785331255347, 0.5275670222350968, 0.2799265605144571, 0.279926560514323, 0.5275670222348438, 0.700378533125195, 0.8245121493330985, 0.8859814447862658, 0.885981444786266, 0.8245121493330978, 0.7003785331251948, 0.5275670222348432, 0.2799265605143228, 0.27992656051414944, 0.5275670222345151, 0.7003785331247554, 0.8245121493325757, 0.885981444785704, 0.8859814447857036, 0.8245121493325756, 0.7003785331247551, 0.5275670222345148, 0.27992656051414916, 0.2799265605139407, 0.5275670222341202, 0.7003785331242259, 0.8245121493319472, 0.8859814447850273, 0.8859814447850267, 0.8245121493319465, 0.7003785331242252, 0.52756702223412, 0.27992656051394055, 0.27992656051370185, 0.5275670222336682, 0.7003785331236203, 0.8245121493312283, 0.885981444784253, 0.8859814447842529, 0.8245121493312276, 0.7003785331236196, 0.527567022233668, 0.27992656051370174, 0.2799265605134385, 0.5275670222331704, 0.7003785331229528, 0.8245121493304355, 0.8859814447834009, 0.8859814447834014, 0.8245121493304352, 0.7003785331229525, 0.5275670222331701, 0.2799265605134385, 0.27992656051315734, 0.5275670222326388, 0.700378533122241, 0.824512149329591, 0.8859814447824915, 0.8859814447824912, 0.8245121493295909, 0.7003785331222411, 0.5275670222326387, 0.27992656051315734, 0.27992656051286463, 0.5275670222320854, 0.7003785331214997, 0.824512149328711, 0.8859814447815446, 0.8859814447815444, 0.8245121493287109, 0.7003785331215001, 0.5275670222320856, 0.27992656051286474, 0.2799265605125681, 0.5275670222315243, 0.7003785331207483, 0.8245121493278198, 0.8859814447805853, 0.8859814447805853, 0.8245121493278198, 0.7003785331207486, 0.5275670222315249, 0.2799265605125682, 0.27992656051227255, 0.5275670222309661, 0.7003785331200013, 0.8245121493269327, 0.8859814447796316, 0.8859814447796316, 0.8245121493269337, 0.7003785331200024, 0.5275670222309667, 0.2799265605122728, 0.27992656051198717, 0.5275670222304258, 0.7003785331192778, 0.824512149326075, 0.885981444778708, 0.8859814447787081, 0.8245121493260753, 0.7003785331192789, 0.5275670222304265, 0.2799265605119875, 0.27992656051171344, 0.5275670222299084, 0.7003785331185864, 0.824512149325254, 0.8859814447778254, 0.8859814447778251, 0.8245121493252549, 0.7003785331185869, 0.5275670222299094, 0.27992656051171394, 0.2799265605114607, 0.5275670222294295, 0.7003785331179423, 0.8245121493244907, 0.8859814447770048, 0.885981444777005, 0.8245121493244916, 0.7003785331179435, 0.5275670222294302, 0.2799265605114612, 0.2799265605112254, 0.5275670222289776, 0.7003785331173382, 0.8245121493237754, 0.8859814447762334, 0.8859814447762339, 0.8245121493237764, 0.7003785331173392, 0.5275670222289783, 0.27992656051122594, 0.27992656051102077, 0.5275670222285856, 0.7003785331168094, 0.8245121493231481, 0.8859814447755574, 0.885981444775558, 0.8245121493231488, 0.7003785331168104, 0.5275670222285866, 0.27992656051102127, 0.2799265605108249, 0.5275670222281772, 0.7003785331162612, 0.8245121493224972, 0.8859814447748545, 0.8859814447748544, 0.8245121493224985, 0.7003785331162622, 0.527567022228178, 0.2799265605108255, 0.27992656051080345, 0.5275670222282155, 0.7003785331163467, 0.8245121493225923, 0.8859814447749603, 0.8859814447749609, 0.824512149322594, 0.7003785331163483, 0.5275670222282166, 0.2799265605108042, 0.27992656051059905, 0.527567022228164, 0.7003785331162979, 0.8245121493225265, 0.8859814447748836, 0.8859814447748836, 0.8245121493225277, 0.7003785331162998, 0.5275670222281655, 0.27992656051059916]]]

        phi_test = np.array(phi_test)

        keff_test = 0.79574521

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        l = 0
        phi = pydgm.state.mg_phi[l, :, :].flatten()
        phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
        np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)
        # np.testing.assert_array_almost_equal(phi_one, phi_one_test, 12)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l0_simple_2(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        self.set_eigen()
        pydgm.control.scatter_leg_order = 0
        pydgm.control.angle_order = 8
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 1.0
        pydgm.control.boundary_south = 1.0
        self.set_mesh('slab')

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[2.0961489847004953, 4.033190945485674, 5.551620460793927, 6.661144459726783, 7.2320066472666245, 7.232006647266628, 6.6611444597267715, 5.551620460793921, 4.033190945485668, 2.0961489847004926, 2.096148984700537, 4.033190945485753, 5.551620460794036, 6.661144459726908, 7.232006647266764, 7.232006647266761, 6.661144459726905, 5.551620460794029, 4.033190945485745, 2.096148984700534, 2.0961489847006134, 4.0331909454859085, 5.551620460794249, 6.6611444597271605, 7.2320066472670455, 7.232006647267039, 6.661144459727161, 5.551620460794241, 4.033190945485902, 2.09614898470061, 2.096148984700733, 4.033190945486129, 5.551620460794558, 6.661144459727534, 7.232006647267451, 7.232006647267447, 6.66114445972753, 5.551620460794552, 4.033190945486123, 2.0961489847007293, 2.0961489847008803, 4.033190945486424, 5.5516204607949575, 6.6611444597280185, 7.232006647267975, 7.232006647267969, 6.661144459728016, 5.551620460794951, 4.033190945486419, 2.0961489847008767, 2.0961489847010624, 4.033190945486767, 5.551620460795439, 6.661144459728597, 7.2320066472686015, 7.2320066472686015, 6.66114445972859, 5.551620460795436, 4.033190945486762, 2.096148984701059, 2.0961489847012644, 4.033190945487167, 5.551620460795982, 6.661144459729254, 7.232006647269314, 7.232006647269314, 6.6611444597292495, 5.551620460795981, 4.033190945487164, 2.096148984701263, 2.096148984701489, 4.033190945487596, 5.551620460796585, 6.661144459729968, 7.232006647270098, 7.232006647270098, 6.661144459729965, 5.551620460796584, 4.033190945487594, 2.096148984701488, 2.0961489847017276, 4.033190945488059, 5.551620460797211, 6.661144459730738, 7.232006647270923, 7.23200664727092, 6.661144459730735, 5.55162046079721, 4.033190945488058, 2.0961489847017276, 2.0961489847019683, 4.0331909454885295, 5.551620460797872, 6.661144459731512, 7.232006647271776, 7.232006647271777, 6.661144459731513, 5.551620460797872, 4.0331909454885295, 2.096148984701969, 2.09614898470222, 4.033190945489003, 5.551620460798518, 6.661144459732309, 7.232006647272627, 7.232006647272626, 6.661144459732311, 5.55162046079852, 4.033190945489006, 2.0961489847022237, 2.096148984702451, 4.033190945489471, 5.5516204607991595, 6.661144459733066, 7.232006647273468, 7.232006647273469, 6.661144459733069, 5.551620460799162, 4.033190945489475, 2.0961489847024546, 2.0961489847026864, 4.033190945489906, 5.551620460799769, 6.6611444597338, 7.2320066472742575, 7.23200664727426, 6.661144459733801, 5.5516204607997715, 4.033190945489912, 2.096148984702691, 2.0961489847028907, 4.033190945490315, 5.551620460800324, 6.661144459734478, 7.232006647274986, 7.232006647274986, 6.661144459734484, 5.551620460800331, 4.0331909454903245, 2.096148984702897, 2.096148984703067, 4.033190945490678, 5.551620460800837, 6.661144459735049, 7.232006647275649, 7.232006647275649, 6.661144459735055, 5.551620460800844, 4.033190945490689, 2.096148984703074, 2.096148984703217, 4.033190945490951, 5.551620460801256, 6.661144459735578, 7.23200664727616, 7.232006647276162, 6.661144459735587, 5.551620460801265, 4.0331909454909605, 2.0961489847032246, 2.0961489847032335, 4.033190945491144, 5.5516204608015665, 6.661144459735901, 7.232006647276537, 7.232006647276543, 6.661144459735912, 5.551620460801579, 4.033190945491156, 2.096148984703242, 2.0961489847031425, 4.033190945491048, 5.551620460801459, 6.661144459735774, 7.2320066472764015, 7.23200664727641, 6.661144459735785, 5.55162046080147, 4.033190945491061, 2.0961489847031514, 2.096148984702825, 4.033190945490437, 5.551620460800661, 6.661144459734727, 7.232006647275304, 7.232006647275312, 6.661144459734738, 5.551620460800671, 4.0331909454904515, 2.0961489847028325, 2.0961489847039614, 4.033190945490715, 5.551620460800366, 6.661144459734989, 7.232006647275477, 7.232006647275481, 6.661144459734999, 5.551620460800376, 4.0331909454907295, 2.0961489847039703]], [[0.2739724962122418, 0.5754374485111884, 0.79994591550689, 0.9618803517876696, 1.0441763702689986, 1.0441763702689986, 0.9618803517876687, 0.799945915506889, 0.5754374485111875, 0.2739724962122413, 0.2739724962122471, 0.5754374485111987, 0.7999459155069055, 0.9618803517876872, 1.0441763702690183, 1.044176370269018, 0.9618803517876869, 0.7999459155069049, 0.5754374485111979, 0.2739724962122466, 0.2739724962122571, 0.5754374485112207, 0.7999459155069346, 0.9618803517877237, 1.0441763702690576, 1.0441763702690572, 0.9618803517877232, 0.7999459155069342, 0.57543744851122, 0.27397249621225644, 0.2739724962122724, 0.5754374485112511, 0.7999459155069794, 0.9618803517877758, 1.0441763702691151, 1.0441763702691147, 0.9618803517877752, 0.7999459155069784, 0.5754374485112504, 0.27397249621227193, 0.2739724962122914, 0.5754374485112929, 0.7999459155070344, 0.9618803517878453, 1.0441763702691886, 1.0441763702691886, 0.9618803517878446, 0.7999459155070339, 0.5754374485112923, 0.2739724962122911, 0.27397249621231495, 0.5754374485113404, 0.7999459155071043, 0.9618803517879249, 1.0441763702692775, 1.0441763702692777, 0.9618803517879247, 0.7999459155071036, 0.5754374485113399, 0.2739724962123147, 0.2739724962123415, 0.5754374485113969, 0.7999459155071795, 0.9618803517880194, 1.0441763702693772, 1.0441763702693774, 0.9618803517880192, 0.7999459155071788, 0.5754374485113967, 0.2739724962123411, 0.27397249621236996, 0.5754374485114563, 0.7999459155072661, 0.9618803517881193, 1.0441763702694886, 1.044176370269489, 0.9618803517881187, 0.7999459155072653, 0.575437448511456, 0.27397249621236985, 0.27397249621240133, 0.5754374485115211, 0.799945915507353, 0.9618803517882293, 1.0441763702696054, 1.0441763702696052, 0.9618803517882293, 0.7999459155073528, 0.5754374485115211, 0.2739724962124014, 0.27397249621243164, 0.575437448511587, 0.7999459155074468, 0.9618803517883373, 1.0441763702697262, 1.0441763702697267, 0.9618803517883376, 0.7999459155074468, 0.5754374485115871, 0.27397249621243175, 0.27397249621246483, 0.5754374485116528, 0.7999459155075375, 0.9618803517884502, 1.0441763702698457, 1.0441763702698454, 0.9618803517884502, 0.7999459155075378, 0.5754374485116532, 0.2739724962124652, 0.2739724962124945, 0.575437448511718, 0.7999459155076273, 0.9618803517885566, 1.044176370269963, 1.0441763702699631, 0.9618803517885572, 0.799945915507628, 0.5754374485117184, 0.273972496212495, 0.27397249621252423, 0.5754374485117777, 0.7999459155077122, 0.9618803517886572, 1.0441763702700744, 1.0441763702700746, 0.9618803517886582, 0.7999459155077129, 0.5754374485117787, 0.27397249621252484, 0.2739724962125526, 0.5754374485118326, 0.7999459155077845, 0.9618803517887524, 1.0441763702701716, 1.0441763702701716, 0.9618803517887529, 0.7999459155077855, 0.5754374485118338, 0.2739724962125532, 0.2739724962125683, 0.5754374485118775, 0.7999459155078519, 0.9618803517888207, 1.0441763702702567, 1.0441763702702571, 0.9618803517888214, 0.7999459155078529, 0.5754374485118787, 0.2739724962125691, 0.27397249621258835, 0.5754374485119061, 0.7999459155078943, 0.9618803517888869, 1.0441763702703133, 1.0441763702703133, 0.961880351788888, 0.7999459155078956, 0.5754374485119075, 0.2739724962125892, 0.27397249621254305, 0.5754374485118984, 0.7999459155079105, 0.9618803517888707, 1.0441763702703089, 1.0441763702703095, 0.9618803517888715, 0.7999459155079119, 0.5754374485118998, 0.27397249621254394, 0.2739724962125052, 0.5754374485118788, 0.7999459155079016, 0.9618803517888538, 1.0441763702702862, 1.044176370270287, 0.9618803517888557, 0.7999459155079033, 0.5754374485118802, 0.27397249621250624, 0.27397249621230524, 0.5754374485116235, 0.7999459155076037, 0.9618803517884091, 1.0441763702698477, 1.0441763702698479, 0.9618803517884107, 0.7999459155076051, 0.5754374485116255, 0.2739724962123061, 0.2739724962130326, 0.5754374485122145, 0.799945915508138, 0.9618803517894161, 1.044176370270817, 1.0441763702708178, 0.9618803517894177, 0.7999459155081399, 0.5754374485122167, 0.2739724962130338]]]

        phi_test = np.array(phi_test)

        keff_test = 0.89883076

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 6)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 6)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l0_vacuum(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        self.set_eigen()
        self.set_mesh('c5g7')
        pydgm.control.scatter_leg_order = 0
        pydgm.control.angle_order = 2
        pydgm.control.boundary_east = 0.0
        pydgm.control.boundary_west = 0.0
        pydgm.control.boundary_north = 0.0
        pydgm.control.boundary_south = 0.0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[0.35081124910427713, 0.6854655499030339, 1.0007249369042757, 1.2985328898630344, 1.563224902743595, 1.7826407144518162, 1.94958500466628, 2.060552043341672, 2.1130992285572154, 2.131217279876635, 2.1265963759495343, 2.0446931287237775, 1.9542228763479557, 1.8750253401679993, 1.7958657595840104, 1.7197773674017947, 1.6410083995810305, 1.550889056740626, 1.4504335630091199, 1.2840986213294407, 0.8503338072265376, 0.39872730496143116, 0.1782003745892477, 0.08073312241073573, 0.034002855533482076, 0.012974693900982152, 0.6854655499030327, 1.3545640865919135, 2.0030354070645795, 2.5960298083231903, 3.125359446101018, 3.570989068899842, 3.9117292343460224, 4.13345218589575, 4.234071333472411, 4.289498193983748, 4.276737574759955, 4.126348339639034, 3.9281230557297335, 3.779780907950062, 3.6288770383449855, 3.4773006775186532, 3.3243509444580495, 3.1358665710968423, 2.9754422054868854, 2.6580813821356646, 1.7493999345488647, 0.7929535290128966, 0.3619950168414859, 0.15965681744144544, 0.07086317351177245, 0.021633286399542134, 1.0007249369042661, 2.0030354070645715, 2.9574512997298443, 3.852515972115808, 4.6411693072709275, 5.3073885989210545, 5.82786683019642, 6.168195888740291, 6.3297543913926315, 6.426113509763409, 6.4251831180072845, 6.1981940027957085, 5.933196448041294, 5.705229630156112, 5.498146250825775, 5.282874945374947, 5.042938898069826, 4.784969938239665, 4.5455828675147165, 4.079972914650367, 2.673685703952814, 1.2006971059175358, 0.5421509836510511, 0.24478395430944788, 0.10064390527925264, 0.03763831739416063, 1.2985328898630197, 2.5960298083231614, 3.8525159721157887, 5.009411128155563, 6.061807968707587, 6.948246166516538, 7.639300245597813, 8.116618765540442, 8.358997065816313, 8.509701749527022, 8.54211948089713, 8.281479811430312, 7.939805464702233, 7.690259293866163, 7.415555948893723, 7.1381218285089645, 6.850345206392396, 6.487482053201081, 6.183488065191449, 5.545403809299508, 3.6340487479152865, 1.6255702420523448, 0.7316617194922722, 0.32194354646184914, 0.14149293091943044, 0.044005230084246644, 1.5632249027435619, 3.1253594461009664, 4.641169307270865, 6.061807968707547, 7.331027418346777, 8.443385191963177, 9.32431102459164, 9.935386493648634, 10.285077324761945, 10.531320983409579, 10.623925131460979, 10.360008670751077, 10.005455288290893, 9.713498205455338, 9.42669298285057, 9.10131760288395, 8.732753905468094, 8.302100438454731, 7.897610408790714, 7.086076234728791, 4.637778202514981, 2.0718407942607264, 0.9188416103399267, 0.41099651839997337, 0.17056515352120627, 0.052736566795399537, 1.782640714451764, 3.5709890688997463, 5.3073885989209435, 6.948246166516425, 8.443385191963104, 9.733931745302655, 10.81958450113743, 11.607281884339052, 12.076946236988505, 12.459493133136379, 12.66984929084216, 12.453228696419774, 12.113892376187607, 11.844888185661901, 11.547926514900388, 11.196966082159168, 10.759448692867958, 10.223058052050387, 9.736418888317562, 8.712047359730064, 5.700527021090216, 2.5246097594624404, 1.125205165628508, 0.48616066754210324, 0.1949254795631784, 0.0800602080069369, 1.9495850046662055, 3.911729234345875, 5.8278668301962275, 7.639300245597614, 9.324311024591463, 10.819584501137323, 12.055836194096287, 13.052305072149407, 13.726206328062654, 14.277231602969998, 14.680237646201023, 14.57743601326566, 14.315722336555705, 14.141073267698482, 13.848402035134352, 13.463294148214421, 12.995432273819779, 12.326268788177437, 11.705581500067145, 10.480289918495936, 6.8099774532194575, 3.0167769439178342, 1.3096566071116464, 0.5449787770097748, 0.25259597606697465, 0.0703043568700002, 2.060552043341548, 4.1334521858955435, 6.1681958887400095, 8.116618765540123, 9.935386493648327, 11.607281884338796, 13.052305072149258, 14.195788714878628, 15.12159412217456, 15.994194119587252, 16.6230432292049, 16.741702212914426, 16.680450721624176, 16.577980159655134, 16.37193442192953, 15.986678597561337, 15.41069183708704, 14.656063839229923, 13.85829155772278, 12.30621792256093, 8.025073316655504, 3.478201732566453, 1.4471473635378582, 0.6559359061288222, 0.2636553174992329, 0.08647456247398817, 2.1130992285570898, 4.234071333472129, 6.329754391392262, 8.358997065815876, 10.28507732476148, 12.0769462369881, 13.726206328062354, 15.121594122174397, 16.22441428714392, 17.459347222223748, 18.65559897964585, 19.177721059462485, 19.326402801619096, 19.436576301912627, 19.315871645188267, 18.948669182669914, 18.29614327779578, 17.331263887964937, 16.378495781560495, 14.506380032955406, 9.219173632911202, 3.816347300383929, 1.6545791825072056, 0.7172516941400257, 0.287281115073383, 0.10398131307467023, 2.131217279876434, 4.289498193983406, 6.426113509762876, 8.509701749526398, 10.531320983408918, 12.459493133135764, 14.277231602969504, 15.994194119586881, 17.45934722222353, 18.93127511385714, 20.469050631497232, 21.41172372480097, 21.938370425102097, 22.28776962966337, 22.287486607985592, 21.922565167021627, 21.23703797828684, 20.075226741442346, 18.847093958954378, 16.46608438425968, 10.13511691136352, 4.188265985299994, 1.8344195295673422, 0.7580990012823184, 0.3278434958930946, 0.10139420903899396, 2.1265963759492785, 4.276737574759457, 6.425183118006623, 8.542119480896293, 10.623925131460112, 12.669849290841308, 14.680237646200244, 16.62304322920424, 18.65559897964535, 20.469050631497005, 21.68823634224059, 22.86092584712057, 23.893753855085407, 24.43770521361033, 24.56574859697057, 24.264350504573287, 23.469438666561807, 22.315454712332652, 20.641324930247023, 17.337542783854968, 10.83584022101105, 4.597502024632544, 1.924653632090281, 0.837228596603349, 0.333363782782968, 0.11634804238437932, 2.044693128723472, 4.126348339638428, 6.198194002794864, 8.281479811429355, 10.360008670749975, 12.45322869641863, 14.577436013264574, 16.74170221291353, 19.17772105946186, 21.411723724800574, 22.86092584712037, 24.18169840767736, 25.540921114922007, 26.35203356015483, 26.610966143895734, 26.31332402119609, 25.52480806134245, 24.249503782019165, 22.13696790053547, 18.38054406299276, 11.413362616963257, 4.897278606334689, 2.033695902443256, 0.8674452497409136, 0.36071650926920806, 0.11055695248049768, 1.9542228763475225, 3.92812305572902, 5.93319644804032, 7.939805464701069, 10.005455288289678, 12.113892376186282, 14.315722336554431, 16.68045072162312, 19.326402801618276, 21.93837042510154, 23.89375385508505, 25.540921114921858, 27.06044498817575, 28.111014672547515, 28.471145791041522, 28.223238503550064, 27.422825789486843, 25.892868492869905, 23.667007660802653, 19.650184444117937, 11.96976852680213, 5.037042334017385, 2.1452212525245318, 0.8784093828405217, 0.37119378242673734, 0.11965129052542582, 1.87502534016764, 3.779780907949209, 5.705229630154996, 7.6902592938648775, 9.713498205454005, 11.844888185660661, 14.141073267697223, 16.57798015965394, 19.43657630191169, 22.287769629662705, 24.437705213609934, 26.352033560154624, 28.11101467254741, 29.218117574343932, 29.70021568014306, 29.522641879050727, 28.585808160973812, 27.05046157153675, 24.700374763436617, 20.4014136596278, 12.401908077361217, 5.126065950082556, 2.1639384639108297, 0.9107638044836679, 0.35891350467935607, 0.1251517815405409, 1.79586575958369, 3.6288770383442746, 5.498146250824514, 7.415555948892301, 9.42669298284918, 11.547926514899158, 13.848402035133358, 16.371934421928515, 19.315871645187404, 22.28748660798512, 24.56574859697026, 26.61096614389534, 28.471145791041387, 29.700215680143224, 30.24669883999888, 30.007324062025972, 29.12358043134551, 27.542694689348647, 25.078903469280153, 20.70937939436685, 12.544761416638986, 5.16213296344057, 2.136438826063663, 0.9022521815238678, 0.36176513263375665, 0.11320415592121823, 1.7197773674014138, 3.4773006775180995, 5.282874945374146, 7.13812182850758, 9.101317602882434, 11.19696608215792, 13.463294148213734, 15.986678597561127, 18.94866918266962, 21.9225651670212, 24.264350504572608, 26.31332402119576, 28.223238503550636, 29.522641879051385, 30.007324062026246, 29.84055446026765, 28.9482528036582, 27.312198661927994, 24.879806414714395, 20.50409178698958, 12.39505948906482, 5.063515360022076, 2.088830202360018, 0.8540232367906286, 0.35537555121457515, 0.1219284345052922, 1.6410083995808076, 3.32435094445773, 5.042938898069641, 6.850345206391975, 8.732753905466913, 10.759448692866792, 12.995432273819366, 15.410691837087441, 18.296143277796276, 21.2370379782863, 23.469438666561356, 25.524808061343535, 27.42282578948831, 28.585808160974675, 29.12358043134604, 28.948252803658477, 28.054310905274203, 26.471843176455256, 24.03927013510567, 19.793830862522245, 11.924950589348795, 4.836215999542637, 1.9536034217380391, 0.8131935210444393, 0.34625598941751934, 0.10506862585457558, 1.5508890567408025, 3.135866571096891, 4.784969938239648, 6.487482053201386, 8.302100438454922, 10.22305805204942, 12.326268788175708, 14.656063839227981, 17.33126388796355, 20.07522674144329, 22.315454712335516, 24.24950378202173, 25.892868492871404, 27.050461571537756, 27.542694689349425, 27.31219866192848, 26.471843176455472, 24.975559792738096, 22.641894622823177, 18.543232775657128, 11.1107218533374, 4.402752556561509, 1.7790714857742316, 0.780528188710859, 0.30936931236463794, 0.10077675940527793, 1.4504335630092489, 2.9754422054867353, 4.545582867514218, 6.183488065190923, 7.8976104087905785, 9.736418888316791, 11.70558150006434, 13.858291557718648, 16.37849578155859, 18.847093958957107, 20.64132493025105, 22.13696790053754, 23.66700766080374, 24.70037476343767, 25.07890346928096, 24.87980641471497, 24.039270135106026, 22.641894622823337, 20.57361293331468, 16.781883224502728, 9.783397520143328, 3.7994970450970915, 1.6366389349728916, 0.6952973309631525, 0.2799712866444533, 0.10055490724769882, 1.2840986213290815, 2.6580813821351823, 4.079972914649697, 5.545403809298471, 7.086076234727616, 8.71204735972964, 10.480289918495547, 12.306217922560903, 14.506380032957468, 16.46608438426144, 17.337542783855064, 18.380544062993035, 19.650184444118615, 20.40141365962846, 20.709379394367488, 20.50409178699004, 19.793830862522587, 18.54323277565734, 16.781883224502803, 13.632851272541012, 7.924142521133728, 3.2171128112970604, 1.442890389764516, 0.5972213874787509, 0.26190268484021967, 0.08282870676237354, 0.8503338072261927, 1.7493999345484754, 2.673685703952391, 3.634048747914727, 4.63777820251434, 5.700527021089788, 6.809977453220441, 8.025073316657986, 9.21917363291306, 10.135116911363587, 10.835840221010235, 11.413362616962804, 11.969768526802277, 12.401908077361492, 12.544761416639245, 12.395059489065114, 11.924950589349026, 11.110721853337553, 9.783397520143415, 7.9241425211337715, 5.2275679911396615, 2.519370555258747, 1.0963369558912404, 0.5064728077745575, 0.20856495727153368, 0.07295286770745095, 0.39872730496142006, 0.792953529012755, 1.2006971059172928, 1.6255702420521754, 2.071840794260557, 2.5246097594623484, 3.016776943917863, 3.4782017325662, 3.8163473003834967, 4.188265985300104, 4.597502024633215, 4.897278606335067, 5.037042334017423, 5.126065950082655, 5.16213296344071, 5.0635153600222305, 4.836215999542774, 4.402752556561615, 3.799497045097166, 3.2171128112971097, 2.51937055525877, 1.5837923163363268, 0.766797729042123, 0.3500391680446574, 0.16569303591719137, 0.050417168150913044, 0.17820037458924348, 0.3619950168414636, 0.5421509836510111, 0.7316617194921453, 0.91884161033987, 1.1252051656284803, 1.3096566071111218, 1.4471473635370955, 1.6545791825069893, 1.8344195295675056, 1.9246536320904664, 2.0336959024436245, 2.145221252524806, 2.163938463910848, 2.136438826063718, 2.088830202360106, 1.9536034217380986, 1.7790714857742895, 1.6366389349729273, 1.442890389764542, 1.0963369558912583, 0.7667977290421293, 0.4926685991442523, 0.23207488470214896, 0.107042361677319, 0.043311526560468064, 0.08073312241070257, 0.15965681744142662, 0.24478395430939628, 0.3219435464618086, 0.4109965183998587, 0.48616066754171217, 0.5449787770095514, 0.6559359061289367, 0.7172516941399448, 0.758099001282128, 0.8372285966033128, 0.8674452497408953, 0.8784093828406514, 0.9107638044838294, 0.9022521815238855, 0.8540232367906676, 0.8131935210444814, 0.7805281887108749, 0.6952973309631739, 0.5972213874787653, 0.5064728077745669, 0.35003916804466184, 0.2320748847021509, 0.15514351891188, 0.06469933898186078, 0.02475929093210807, 0.03400285553349382, 0.07086317351172622, 0.10064390527922167, 0.14149293091938153, 0.17056515352102278, 0.19492547956312833, 0.2525959760669857, 0.2636553174990806, 0.28728111507331466, 0.3278434958930815, 0.33336378278292483, 0.3607165092692291, 0.3711937824267021, 0.35891350467937927, 0.3617651326338473, 0.3553755512145773, 0.34625598941752783, 0.30936931236465853, 0.2799712866444571, 0.26190268484022844, 0.20856495727153848, 0.16569303591719348, 0.10704236167732, 0.0646993389818615, 0.04696630921338623, 0.010460079769685137, 0.012974693900958387, 0.02163328639955434, 0.037638317394142466, 0.044005230084151296, 0.05273656679543157, 0.08006020800696222, 0.07030435686990835, 0.0864745624739496, 0.10398131307464484, 0.1013942090389945, 0.116348042384385, 0.1105569524804695, 0.11965129052545753, 0.12515178154052223, 0.1132041559212005, 0.12192843450533813, 0.10506862585457459, 0.10077675940527663, 0.10055490724770742, 0.08282870676237288, 0.07295286770745368, 0.050417168150913676, 0.04331152656046867, 0.024759290932108106, 0.01046007976968545, 0.012376216509537921]], [[0.04225797869926791, 0.0875189918545539, 0.13267820955851692, 0.1706568038659617, 0.20545716862591448, 0.23546004222407999, 0.25576407805762597, 0.2698443352644858, 0.26312663809727516, 0.19653131712315572, 0.08241068189057857, 0.042525880748205236, 0.04837265192026308, 0.04548865727927355, 0.0434088339668579, 0.04143476116714869, 0.0396970500046763, 0.03996062341827696, 0.02199501642501735, 0.08916489504164932, 0.416047565130122, 0.5861560793410304, 0.4302624935443886, 0.25861439865400027, 0.1339588528370959, 0.04422856280673793, 0.08751899185455372, 0.19763219950953337, 0.2897198071127156, 0.37948460381452925, 0.4554199229976271, 0.5197954423069022, 0.5704669319516282, 0.5966326531831954, 0.5884995383105188, 0.4344202061945717, 0.1826025732092545, 0.08952112806560417, 0.10928059270281891, 0.09733578894639275, 0.09596843026928589, 0.09251526989647595, 0.08391775286768537, 0.09326397758963918, 0.04136508989899495, 0.2091638496064392, 1.016191562567592, 1.4513854284284258, 1.0678345019458595, 0.646172613343302, 0.33199514471338665, 0.11136910930749863, 0.13267820955851606, 0.2897198071127144, 0.43609433775393125, 0.5631812465489825, 0.6823438735771974, 0.7791831419004199, 0.8530744207288817, 0.8996189202795778, 0.8825668933812694, 0.6538934385556285, 0.27142453822914675, 0.13582954677602269, 0.1597913532100348, 0.1480603165289302, 0.142798981959299, 0.13794422279361995, 0.12898964006125885, 0.13689742929912047, 0.06452610077618653, 0.32279174443103864, 1.5925911080997335, 2.285542844327305, 1.6935452872491623, 1.0226209850995913, 0.5274404527106856, 0.1756542491133897, 0.1706568038659596, 0.37948460381452576, 0.5631812465489794, 0.7386823250310854, 0.8877221794682132, 1.0211857461564766, 1.1215397554910265, 1.1809265149326662, 1.1673577879502748, 0.8634790297555393, 0.36288264168513756, 0.17922513840781495, 0.2177110361824051, 0.19725714663912025, 0.1945558408391191, 0.18741896338392514, 0.1730143024279827, 0.19030873480816965, 0.08379266609983754, 0.4431220766397818, 2.1719600590718593, 3.1220037789543547, 2.3118350194746182, 1.3968940096528186, 0.7177524110029477, 0.23856611312665776, 0.20545716862591065, 0.4554199229976196, 0.682343873577189, 0.8877221794682068, 1.0805733607331391, 1.2366812189233574, 1.3682462628624008, 1.4490328571920597, 1.431948836644845, 1.067961947308677, 0.44714468626722303, 0.22700216193793585, 0.2708074084983021, 0.2508075835622847, 0.24493275997850786, 0.2389703769498603, 0.22102737684357768, 0.2394293327273707, 0.11166308614827229, 0.5601111438065092, 2.7693927941819387, 3.970740659021246, 2.935105072256404, 1.766097301199182, 0.9040449636583179, 0.3017609425967875, 0.23546004222407338, 0.5197954423068891, 0.7791831419004032, 1.021185746156461, 1.2366812189233465, 1.4347399721447072, 1.5822790551326236, 1.6894561480486678, 1.6859347746023812, 1.2555197860724536, 0.5362285746466177, 0.2740748208732178, 0.3303098730601722, 0.30786243531798907, 0.30369435347734225, 0.29399058661764343, 0.2764335353508754, 0.2977257727972531, 0.13517309832563196, 0.6967612481903332, 3.3825448008808414, 4.843541026512959, 3.5595888592500953, 2.1290945792910945, 1.089309418632222, 0.35941235035452745, 0.2557640780576159, 0.5704669319516076, 0.8530744207288545, 1.1215397554909974, 1.368246262862376, 1.5822790551326082, 1.775243365716061, 1.8931216055714892, 1.90425384795817, 1.4403798980740465, 0.6061320485200746, 0.3134285010522567, 0.3844465021135946, 0.35611078914080113, 0.35500843205984345, 0.3483263990737822, 0.3193802056259066, 0.3548122209388014, 0.15896822273381558, 0.8114961409889507, 4.02636070692955, 5.728874442196378, 4.180579183325774, 2.4896364920077008, 1.2613527736073054, 0.42220966479480143, 0.26984433526447166, 0.5966326531831656, 0.8996189202795373, 1.1809265149326207, 1.449032857192015, 1.6894561480486312, 1.8931216055714668, 2.0709239585099484, 2.088154528165788, 1.579757090308119, 0.7125078581334975, 0.40027391418442776, 0.4729084794072594, 0.45827992869763656, 0.4528489055178287, 0.4447529737714183, 0.4219069723779913, 0.4400411653227785, 0.22716907162145628, 1.0016245144662852, 4.674570801958241, 6.62726148910307, 4.801370206513919, 2.822964994746634, 1.436873239405561, 0.471546966571337, 0.26312663809725745, 0.5884995383104814, 0.8825668933812171, 1.167357787950214, 1.4319488366447835, 1.685934774602326, 1.904253847958129, 2.0881545281657647, 2.2133400901989364, 1.706345901215923, 0.6875865473451099, 0.3239978557036775, 0.42569243312780536, 0.395314800064815, 0.401198216123196, 0.3916111821987629, 0.36229034516843545, 0.41513200281329105, 0.12159203336066238, 1.015720797010352, 5.373717211883822, 7.568849666302326, 5.366240263989846, 3.152523669875206, 1.5895327887564097, 0.5221132869535088, 0.19653131712314115, 0.4344202061945394, 0.6538934385555837, 0.8634790297554857, 1.0679619473086224, 1.2555197860724034, 1.4403798980740052, 1.5797570903080909, 1.7063459012159101, 1.5175012689170977, 0.9731116264979799, 0.8647844980287412, 0.9866485038676276, 0.9834046901024974, 0.9894019230730957, 0.985955058770682, 0.9248951866161862, 0.9589333914139672, 0.6991544120111912, 1.722199042512448, 6.367585344887919, 8.43607536567311, 5.896085156975341, 3.4508022540185452, 1.7221115293047367, 0.5719072820909704, 0.08241068189057008, 0.18260257320923823, 0.2714245382291231, 0.3628826416851101, 0.4471446862671939, 0.53622857464659, 0.6061320485200502, 0.7125078581334785, 0.6875865473450979, 0.9731116264979737, 1.8323236006082222, 2.349143290378416, 2.4929894128624017, 2.579105247004903, 2.5974298709174617, 2.561876775952605, 2.496936065053935, 2.3699092600555356, 2.2991992173498406, 3.591418105071652, 7.585701965958078, 9.166818479278078, 6.3916138045141855, 3.687238067692964, 1.848701802466671, 0.6020760074776643, 0.042525880748198776, 0.08952112806558865, 0.13582954677600323, 0.17922513840779086, 0.2270021619379099, 0.274074820873191, 0.31342850105223036, 0.400273914184407, 0.3239978557036582, 0.8647844980287295, 2.349143290378405, 3.333619990387748, 3.575315787108942, 3.709451246877652, 3.748828644083784, 3.711248403052476, 3.608780167402971, 3.4233607689821386, 3.461963606534321, 4.823580426171687, 8.612987650039525, 9.816670663965219, 6.776215702005471, 3.8883052107671063, 1.9362168927196284, 0.6332461591825364, 0.04837265192025263, 0.10928059270280092, 0.1597913532100085, 0.21771103618237655, 0.27080740849827195, 0.33030987306014187, 0.38444650211356474, 0.47290847940723524, 0.4256924331277862, 0.9866485038676159, 2.4929894128623826, 3.575315787108926, 3.9516618445465483, 4.094889421427358, 4.157817153534774, 4.131286493609789, 3.9941228431462403, 3.850878305766585, 3.8318029247712957, 5.2239845188543095, 9.230740712714114, 10.345309778782626, 7.0386623069232295, 4.030595761290104, 1.9929979570365441, 0.6525273643778033, 0.04548865727926454, 0.09733578894637032, 0.14806031652890148, 0.19725714663908517, 0.2508075835622503, 0.307862435317955, 0.35611078914076694, 0.4582799286976088, 0.3953148000647899, 0.9834046901024893, 2.5791052470048808, 3.709451246877623, 4.094889421427346, 4.293039020946489, 4.363323919041531, 4.3230693689464275, 4.216812949380874, 4.029110066565902, 4.004352205523874, 5.457183208876848, 9.546673688612675, 10.648445979878677, 7.189165981290645, 4.091096848374636, 2.0214824421989284, 0.656609528143047, 0.0434088339668493, 0.09596843026926599, 0.14279898195926657, 0.19455584083908142, 0.2449327599784655, 0.3036943534773069, 0.35500843205981075, 0.4528489055178043, 0.4011982161231661, 0.989401923073081, 2.5974298709174337, 3.748828644083747, 4.157817153534771, 4.363323919041551, 4.4358087596639315, 4.418046281712249, 4.286682633022324, 4.1023385967014825, 4.0793781060563425, 5.524010426546714, 9.642471738593331, 10.707476387645517, 7.19684350902358, 4.076365647451872, 2.0084574224186156, 0.6545790463725177, 0.04143476116714053, 0.09251526989646308, 0.13794422279360144, 0.18741896338389577, 0.23897037694983023, 0.29399058661761923, 0.34832639907377105, 0.44475297377141904, 0.3916111821987429, 0.9859550587706765, 2.5618767759525722, 3.7112484030524775, 4.131286493609847, 4.323069368946498, 4.418046281712288, 4.384891190257265, 4.2616798939923495, 4.080274203523238, 4.036393807645437, 5.468810308650263, 9.506407218818161, 10.532338537385087, 7.047391048407422, 3.9810428843593977, 1.961082438971249, 0.63752403226734, 0.03969705000466462, 0.08391775286766047, 0.12898964006122776, 0.1730143024279353, 0.2210273768435068, 0.27643353535080123, 0.31938020562581987, 0.4219069723779321, 0.36229034516835495, 0.924895186616157, 2.4969360650539767, 3.608780167403069, 3.994122843146378, 4.216812949380997, 4.286682633022399, 4.261679893992386, 4.142379903827174, 3.952624359132821, 3.918285785129011, 5.275848775402789, 9.1576263422014, 10.112420510041666, 6.750940893550401, 3.8088266455319437, 1.875011527542191, 0.6129445181876421, 0.03996062341826835, 0.09326397758962543, 0.13689742929909435, 0.19030873480814, 0.23942933272732284, 0.29772577279717394, 0.35481222093870063, 0.44004116532268117, 0.4151320028131923, 0.9589333914139597, 2.3699092600556577, 3.423360768982378, 3.850878305766821, 4.029110066566067, 4.102338596701598, 4.080274203523317, 3.952624359132859, 3.772533663091238, 3.7257559347867297, 5.00995579454167, 8.617505492205039, 9.491960854688413, 6.31803717323621, 3.560663471649663, 1.7624217840617191, 0.572824917674085, 0.02199501642495105, 0.04136508989881882, 0.06452610077589337, 0.0837926660994378, 0.11166308614776849, 0.1351730983249727, 0.15896822273296635, 0.227169071620545, 0.12159203335995995, 0.6991544120109054, 2.2991992173499174, 3.4619636065345163, 3.8318029247714356, 4.00435220552398, 4.079378106056432, 4.0363938076454975, 3.9182857851290507, 3.725755934786751, 3.633018538488494, 4.772682945531031, 8.066903352309888, 8.72823636778331, 5.747120815041379, 3.2637984637120554, 1.6172100254689925, 0.5276922855574209, 0.08916489504168489, 0.20916384960653292, 0.3227917444312073, 0.4431220766400178, 0.5601111438068447, 0.6967612481908058, 0.8114961409895664, 1.0016245144668685, 1.0157207970110083, 1.7221990425128706, 3.591418105071941, 4.823580426171911, 5.223984518854456, 5.4571832088769945, 5.5240104265468295, 5.468810308650341, 5.275848775402865, 5.009955794541736, 4.772682945531074, 5.534969523541939, 7.810507822534237, 7.783528063953942, 5.093969126845078, 2.9255264927268603, 1.4475206461356156, 0.48021070417712713, 0.4160475651302579, 1.0161915625679954, 1.59259110810048, 2.171960059072982, 2.7693927941835166, 3.382544800883152, 4.026360706932757, 4.674570801961788, 5.373717211886597, 6.367585344889167, 7.585701965958411, 8.612987650039708, 9.230740712714326, 9.546673688612882, 9.642471738593517, 9.506407218818328, 9.157626342201553, 8.617505492205163, 8.066903352309966, 7.810507822534271, 7.55440302358814, 6.301306327624733, 4.200328455356228, 2.4106238111767047, 1.2212342217097836, 0.3996270243003227, 0.5861560793409765, 1.4513854284283065, 2.285542844327168, 3.1220037789542667, 3.970740659021294, 4.843541026513222, 5.728874442196864, 6.627261489103659, 7.568849666302843, 8.436075365673553, 9.166818479278437, 9.816670663965493, 10.345309778782875, 10.648445979878925, 10.707476387645762, 10.532338537385327, 10.112420510041881, 9.49196085468858, 8.728236367783428, 7.783528063954025, 6.301306327624777, 4.562056310533262, 3.054401772355386, 1.7989132095590923, 0.9209796754851262, 0.31025005486931045, 0.4302624935441466, 1.0678345019452389, 1.6935452872481436, 2.31183501947323, 2.9351050722546526, 3.5595888592478566, 4.180579183322985, 4.8013702065110255, 5.366240263987782, 5.896085156974593, 6.39161380451431, 6.776215702005813, 7.038662306923557, 7.189165981290942, 7.196843509023856, 7.047391048407673, 6.750940893550611, 6.318037173236383, 5.747120815041508, 5.0939691268451766, 4.200328455356286, 3.054401772355402, 2.02982741597596, 1.2419152332585688, 0.6494112544070322, 0.22037388984070166, 0.25861439865385755, 0.6461726133429478, 1.0226209850990289, 1.3968940096520228, 1.7660973011981183, 2.1290945792898164, 2.4896364920064022, 2.8229649947455266, 3.1525236698743235, 3.4508022540179066, 3.6872380676926615, 3.888305210767134, 4.0305957612902965, 4.091096848374836, 4.076365647452052, 3.981042884359561, 3.8088266455320827, 3.560663471649777, 3.263798463712142, 2.9255264927269287, 2.410623811176748, 1.7989132095591105, 1.2419152332585741, 0.7726903439306204, 0.42228159068501125, 0.14310841763276388, 0.1339588528370151, 0.3319951447131847, 0.5274404527103601, 0.7177524110024893, 0.9040449636577389, 1.0893094186315941, 1.261352773606727, 1.4368732394050578, 1.5895327887559718, 1.7221115293043725, 1.8487018024664292, 1.9362168927195376, 1.9929979570365697, 2.0214824421990163, 2.008457422418712, 1.9610824389713375, 1.8750115275422687, 1.762421784061781, 1.6172100254690414, 1.4475206461356542, 1.22123422170981, 0.9209796754851386, 0.6494112544070366, 0.42228159068501225, 0.2320311983016864, 0.08375826018377389, 0.04422856280670103, 0.11136910930740349, 0.17565424911322775, 0.23856611312643644, 0.30176094259653863, 0.3594123503542533, 0.4222096647944587, 0.4715469665709649, 0.5221132869532258, 0.5719072820908344, 0.602076007477616, 0.6332461591825088, 0.6525273643777897, 0.6566095281430548, 0.6545790463725449, 0.6375240322673696, 0.612944518187668, 0.5728249176741076, 0.5276922855574376, 0.48021070417714096, 0.3996270243003329, 0.3102500548693144, 0.22037388984070316, 0.14310841763276463, 0.08375826018377393, 0.027913683611338194]]]

        phi_test = np.array(phi_test)

        keff_test = 1.01043329

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            phi = pydgm.state.mg_phi[l, :, :].flatten()
            phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
            np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l1(self):
        '''
        Test eigenvalue source problem with reflective conditions and 2g
        '''

        # Set the variables for the test
        self.set_mesh('c5g7')
        self.set_eigen()
        pydgm.control.scatter_leg_order = 1

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[37.07600674374294, 36.746773957956165, 36.089188107116456, 35.10887587952274, 33.80716373229718, 32.198834705553985, 30.27943395241796, 28.108485310424555, 25.62701573597315, 23.341341247388872, 21.143238719428158, 18.32846199375169, 15.751437533793133, 13.717666824772149, 11.911640771657911, 10.375975337324295, 9.064048322166602, 7.872064582112495, 6.992868706625399, 6.060816859359126, 4.058683148042351, 2.249028623892657, 1.342887035914808, 0.7415130716248179, 0.42085959506987225, 0.1839440660089069, 36.74677395795608, 36.421178570613215, 35.77302932387394, 34.803025362159026, 33.51910322859463, 31.93028547697199, 30.03353895576326, 27.88692658388475, 25.435136255837257, 23.176114411287372, 21.00230585532801, 18.217044366727233, 15.666685087573473, 13.653375638001915, 11.863137884679201, 10.34137835996734, 9.040389931385048, 7.8558883456981965, 6.981946734905621, 6.053189515030547, 4.055137081947628, 2.2476664812685936, 1.3415824441046427, 0.7413775607385755, 0.4203459800607337, 0.18381106074387676, 36.089188107116186, 35.77302932387379, 35.138750678660216, 34.19679404811136, 32.94175682550668, 31.392891761150544, 29.543005837966184, 27.449804234582572, 25.05118445966615, 22.845141168379413, 20.72577555491174, 17.99820190175815, 15.498840094757183, 13.526018198903829, 11.772655223751904, 10.276318362694703, 8.994582229549042, 7.825398664816008, 6.962077606559976, 6.041517730296744, 4.048102228442022, 2.244433766015891, 1.3407976803707884, 0.7396151816104753, 0.4198321401298828, 0.1833469594709128, 35.1088758795223, 34.80302536215866, 34.19679404811116, 33.28635099730645, 32.08359042943322, 30.592698097142655, 28.810696384233196, 26.792646429223705, 24.483386860583455, 22.358533874404728, 20.311738931909776, 17.673990287022367, 15.254857780212406, 13.344656291381426, 11.638374446061862, 10.182829655351876, 8.932546374445979, 7.784336877419431, 6.935205664776618, 6.022564548121368, 4.040016823418067, 2.241269663237427, 1.3370694134044654, 0.7386731841212614, 0.4183686764091644, 0.18284595806970277, 33.80716373229648, 33.519103228594055, 32.94175682550628, 32.083590429432995, 30.940473805044647, 29.529034896915014, 27.841847834483364, 25.928016462549333, 23.728333971923288, 21.71216326487558, 19.780042597612482, 17.260641754844595, 14.94449029862743, 13.115027221438856, 11.480426574683037, 10.074973535651322, 8.86092721013578, 7.740292436509801, 6.909486334058236, 6.0096547205708655, 4.030783726637087, 2.2357007760884486, 1.3350277918124818, 0.735390498268569, 0.41678113603385125, 0.18172714453363897, 32.198834705553075, 31.930285476971143, 31.392891761149862, 30.59269809714217, 29.529034896914773, 28.21430477365708, 26.640632619648095, 24.858132690882655, 22.807720198052454, 20.930609737553453, 19.12034535290535, 16.75229407262212, 14.574617759488582, 12.849663440445541, 11.296767654694175, 9.954665901983091, 8.787335487385203, 7.69728181962532, 6.882694342798136, 5.990543683611482, 4.024496865129248, 2.232041792553683, 1.3290757833043205, 0.732025530199424, 0.4140225523885309, 0.18081589581791305, 30.279433952416824, 30.03353895576221, 29.543005837965264, 28.81069638423246, 27.84184783448283, 26.640632619647825, 25.206403761632526, 23.58124537715391, 21.702176241300485, 19.999191190815335, 18.38101957156058, 16.203694759570528, 14.183167642163243, 12.582941844155357, 11.128031246971808, 9.856215306293311, 8.739413740590667, 7.678946189717443, 6.883509393520359, 6.000469698524295, 4.02054599195191, 2.223965737778478, 1.322702724422884, 0.7263377511206172, 0.41089248877631834, 0.1790586258122789, 28.10848531042319, 27.886926583883476, 27.449804234581425, 26.79264642922274, 25.92801646254857, 24.858132690882115, 23.58124537715366, 22.139225981662843, 20.474186384359783, 18.96879994282763, 17.51817190356208, 15.560835495125188, 13.742940373352674, 12.291476804252087, 10.949967446299777, 9.759688973996541, 8.6976615517982, 7.667424307812988, 6.881115260190779, 5.9903701580577815, 4.019893414843968, 2.215143598026757, 1.3107884398081948, 0.719884958410797, 0.4058676020958557, 0.17706887964843854, 25.627015735971582, 25.43513625583575, 25.05118445966478, 24.483386860582222, 23.728333971922247, 22.807720198051648, 21.702176241299938, 20.474186384359527, 19.040128768330188, 17.794348725160397, 16.66657433532905, 15.012700707410838, 13.424817148890595, 12.13416363133544, 10.9058137928547, 9.793226016200212, 8.779790232412251, 7.772011366611211, 6.989127500485838, 6.080122804824655, 4.026084778527788, 2.1870929933103, 1.299016619427444, 0.708150310133997, 0.40183289403860983, 0.1726932155361381, 23.341341247387188, 23.176114411285724, 22.84514116837789, 22.358533874403342, 21.712163264874366, 20.930609737552444, 19.99919119081458, 18.968799942827157, 17.794348725160194, 16.700910102710118, 15.721358434677082, 14.391760270669279, 13.09806474836534, 11.966554355933438, 10.868181808772771, 9.83440725029527, 8.869690082380366, 7.894841223090035, 7.102824896755519, 6.116654503927478, 3.973686603475489, 2.153990660919749, 1.2801365822200967, 0.6950769022630827, 0.39486945209590607, 0.1689525837049083, 21.14323871942609, 21.00230585532604, 20.725775554909866, 20.311738931908025, 19.78004259761091, 19.120345352903968, 18.38101957155944, 17.51817190356125, 16.666574335328548, 15.721358434676894, 14.453820786464977, 13.367515216393276, 12.421498551721474, 11.451494829210642, 10.516659098376113, 9.586156603409515, 8.689431339298453, 7.7835490309471975, 6.951271485495275, 5.805026639540571, 3.849955138127568, 2.131727252112101, 1.24285961701425, 0.6862436081980507, 0.3808740453795962, 0.1687437519798721, 18.328461993749066, 18.217044366724657, 17.998201901755664, 17.673990287019983, 17.260641754842368, 16.75229407262005, 16.2036947595687, 15.560835495123712, 15.012700707409879, 14.391760270668865, 13.367515216393182, 12.491261920544972, 11.788375285242081, 10.98789278215211, 10.186499572475446, 9.353744442076135, 8.519493929591833, 7.665265454963887, 6.812327040983043, 5.630378254470469, 3.726936869009445, 2.082310164968144, 1.2077172882918579, 0.6680847956043909, 0.36884795740287596, 0.16421351475632398, 15.751437533790222, 15.666685087570604, 15.498840094754394, 15.254857780209681, 14.944490298624798, 14.574617759486069, 14.183167642160909, 13.742940373350768, 13.424817148889375, 13.098064748364829, 12.421498551721346, 11.788375285242019, 11.258901013016754, 10.608111738145743, 9.912379497774753, 9.164090118298311, 8.388874692457838, 7.567267585488658, 6.737976202628842, 5.5681014436095895, 3.630952733233592, 2.0079060549514383, 1.1705841210289207, 0.6421924200785684, 0.35716614607178426, 0.15671921925877055, 13.717666824769239, 13.65337563799904, 13.526018198901005, 13.344656291378637, 13.115027221436108, 12.849663440442846, 12.582941844152783, 12.291476804249946, 12.134163631334223, 11.966554355933077, 11.451494829210601, 10.987892782152054, 10.608111738145707, 10.085937315773073, 9.495978598121884, 8.831160660776394, 8.118806713131999, 7.34572997935345, 6.5452616160683075, 5.3922095862353965, 3.51243525224029, 1.9292633209324843, 1.1210837270752723, 0.614534999166671, 0.3413239109975868, 0.14933527188363352, 11.911640771655035, 11.863137884676352, 11.772655223749068, 11.638374446059059, 11.480426574680228, 11.296767654691354, 11.12803124696896, 10.949967446297102, 10.905813792853529, 10.868181808772988, 10.516659098376321, 10.186499572475483, 9.912379497774737, 9.49597859812192, 8.994756542940753, 8.40499120960994, 7.759153809963699, 7.034767741305219, 6.279195887063525, 5.178847702278754, 3.356294622787179, 1.8357503698889959, 1.0640729173733878, 0.5818552254826955, 0.3228862381586656, 0.14147016503555057, 10.375975337321528, 10.34137835996458, 10.276318362691947, 10.182829655349133, 10.074973535648574, 9.954665901980325, 9.856215306290455, 9.75968897399394, 9.793226016199181, 9.834407250295573, 9.586156603409796, 9.353744442076222, 9.164090118298331, 8.831160660776456, 8.404991209609973, 7.887070540316959, 7.304486915209825, 6.638910646878311, 5.929970630939191, 4.8865053181468765, 3.1675572132018965, 1.7257225095646198, 0.9959280606533345, 0.5448745858650221, 0.3021243088235252, 0.13285600543896028, 9.064048322163922, 9.040389931382368, 8.994582229546374, 8.932546374443312, 8.860927210133141, 8.787335487382691, 8.739413740588343, 8.697661551796227, 8.779790232411, 8.869690082380089, 8.689431339298677, 8.519493929591938, 8.38887469245787, 8.118806713132065, 7.759153809963742, 7.304486915209843, 6.781347564036856, 6.17387713839439, 5.523648224251518, 4.553502305990615, 2.9380276950452084, 1.5934430400651123, 0.9205437817084973, 0.5021135414573535, 0.2800432388508868, 0.12238320355197387, 7.872064582109958, 7.855888345695664, 7.825398664813475, 7.784336877416901, 7.740292436507322, 7.6972818196231, 7.678946189715786, 7.667424307811396, 7.772011366609638, 7.894841223089576, 7.783549030947501, 7.665265454964007, 7.567267585488667, 7.345729979353489, 7.0347677413052505, 6.63891064687833, 6.173877138394396, 5.632234699822551, 5.041441181122201, 4.149179752784209, 2.6710892197042417, 1.4409322030199712, 0.8331813467750278, 0.4575211299770513, 0.2548774942626548, 0.11207315210354195, 6.992868706622855, 6.981946734903087, 6.962077606557435, 6.935205664774083, 6.909486334055695, 6.882694342795747, 6.883509393518934, 6.881115260189655, 6.989127500484442, 7.102824896755041, 6.951271485495448, 6.812327040983048, 6.737976202628771, 6.5452616160683075, 6.2791958870635405, 5.9299706309391995, 5.523648224251523, 5.0414411811222015, 4.527372362959921, 3.72409983729575, 2.3546120758682934, 1.2632224470048339, 0.7420845718304506, 0.407451905750255, 0.23015733748682277, 0.10030042848440891, 6.060816859356861, 6.053189515028297, 6.041517730294488, 6.022564548119102, 6.009654720568529, 5.990543683609099, 6.000469698523158, 5.990370158057207, 6.080122804823762, 6.11665450392712, 5.805026639540473, 5.6303782544703465, 5.568101443609492, 5.39220958623541, 5.1788477022787855, 4.88650531814691, 4.553502305990646, 4.149179752784241, 3.7240998372957836, 3.072436276480318, 1.9613474893035805, 1.0790145953771975, 0.6445824412232548, 0.35755844201568904, 0.2035697679899881, 0.0890197350369814, 4.058683148041033, 4.055137081946319, 4.0481022284407135, 4.040016823416763, 4.030783726635768, 4.024496865127963, 4.020545991951319, 4.0198934148436996, 4.026084778527356, 3.9736866034752643, 3.8499551381274286, 3.7269368690093407, 3.63095273323354, 3.512435252240299, 3.356294622787209, 3.167557213201934, 2.9380276950452444, 2.671089219704273, 2.3546120758683213, 1.9613474893035903, 1.4038062205637845, 0.8512106945968637, 0.5090838678650927, 0.2964026156216917, 0.16575776737624576, 0.07676923369225463, 2.2490286238920305, 2.2476664812679705, 2.2444337660152804, 2.241269663236839, 2.235700776087898, 2.2320417925532174, 2.223965737778172, 2.215143598026534, 2.1870929933100713, 2.1539906609195714, 2.1317272521119723, 2.0823101649680504, 2.0079060549513725, 1.929263320932436, 1.835750369888964, 1.725722509564594, 1.5934430400650905, 1.4409322030199498, 1.2632224470048141, 1.0790145953771746, 0.851210694596847, 0.5782877918801945, 0.36274482354426685, 0.219389514832413, 0.12501577546417905, 0.058973037275797495, 1.3428870359144096, 1.3415824441042508, 1.3407976803704105, 1.3370694134041061, 1.3350277918121558, 1.3290757833040325, 1.3227027244226484, 1.3107884398080025, 1.2990166194272839, 1.2801365822199675, 1.2428596170141466, 1.2077172882917744, 1.1705841210288546, 1.1210837270752219, 1.0640729173733463, 0.9959280606532993, 0.9205437817084682, 0.8331813467750044, 0.7420845718304329, 0.6445824412232366, 0.5090838678650765, 0.3627448235442627, 0.24384828091200203, 0.15269210150833368, 0.09004047054871722, 0.04258305588493556, 0.7415130716246069, 0.7413775607383695, 0.7396151816102758, 0.7386731841210746, 0.7353904982683963, 0.7320255301992701, 0.7263377511204834, 0.7198849584106805, 0.7081503101338933, 0.6950769022629929, 0.6862436081979744, 0.6680847956043265, 0.6421924200785137, 0.6145349991666224, 0.5818552254826546, 0.544874585864987, 0.5021135414573229, 0.4575211299770257, 0.40745190575023477, 0.35755844201566983, 0.29640261562167847, 0.21938951483240812, 0.15269210150833235, 0.1000565359306431, 0.060241837392415114, 0.029212804712447634, 0.420859595069738, 0.4203459800606018, 0.41983214012975617, 0.41836867640904346, 0.41678113603373884, 0.4140225523884266, 0.41089248877622486, 0.4058676020957734, 0.40183289403853967, 0.39486945209584473, 0.38087404537954395, 0.36884795740283066, 0.357166146071745, 0.3413239109975542, 0.32288623815863665, 0.3021243088235005, 0.2800432388508669, 0.2548774942626385, 0.23015733748681028, 0.20356976798997764, 0.16575776737623654, 0.12501577546417567, 0.09004047054871575, 0.06024183739241481, 0.03759577925978396, 0.01814998640121104, 0.18394406600884156, 0.1838110607438126, 0.18334695947085006, 0.18284595806964335, 0.18172714453358246, 0.1808158958178629, 0.17905862581223322, 0.177068879648395, 0.1726932155360953, 0.16895258370487137, 0.16874375197984157, 0.16421351475629895, 0.1567192192587483, 0.1493352718836125, 0.1414701650355334, 0.13285600543894602, 0.12238320355196136, 0.11207315210353187, 0.10030042848440089, 0.08901973503697416, 0.07676923369225046, 0.05897303727579571, 0.04258305588493505, 0.02921280471244727, 0.01814998640121099, 0.009233208092604517]], [[5.501669330377667, 5.452166805329012, 5.355906968633817, 5.207706899856233, 5.01754752142975, 4.76867208405677, 4.482035392397156, 4.092177812979152, 3.5944469496492464, 2.5239026863053655, 0.9669822247519397, 0.4039021292775377, 0.43440683664390123, 0.3485247128319119, 0.31514042944848963, 0.2715313622753057, 0.2311192663200511, 0.22208179668415276, 0.1229971114926461, 0.5031091121895412, 2.471489308914018, 3.7416525496832933, 3.2298487314470283, 2.319621105456953, 1.393540176382845, 0.5497551443388494, 5.452166805328994, 5.403487408780861, 5.308080267145268, 5.16217722020698, 4.9740002237473115, 4.728363221752975, 4.445101903956707, 4.059698527708874, 3.566527134266773, 2.505028488682218, 0.9610656476261003, 0.4024410803752412, 0.4328001578377332, 0.3475507741640543, 0.31456669772979035, 0.2712408323864328, 0.23104207019966208, 0.22208236379269505, 0.12335175265859048, 0.5033862627667269, 2.4698115274741506, 3.7391992854436253, 3.227857568126471, 2.3179375117762193, 1.3924762350307736, 0.5492241381108233, 5.35590696863378, 5.308080267145239, 5.215751090745451, 5.0726366811106125, 4.889915429189729, 4.649785803304535, 4.3734524320813595, 3.996207957646158, 3.5137731690097582, 2.4692657980427137, 0.9461037318756599, 0.3959263031268452, 0.42639295614905465, 0.34306048439894593, 0.31053080349243867, 0.2683706660760165, 0.22861378175845623, 0.22038979616033474, 0.12161488522095949, 0.5011115173697529, 2.4665614232092117, 3.7347546667156815, 3.223688846540459, 2.3147261952800027, 1.3900696725140187, 0.5483331806849158, 5.20770689985616, 5.162177220206932, 5.072636681110582, 4.936090411048448, 4.7595140211675835, 4.5290268032481045, 4.262932982096157, 3.8989230086418987, 3.430609940837083, 2.413047288119813, 0.9290695339820086, 0.3922037757735757, 0.42225669284769957, 0.34085529258370717, 0.3094169121097974, 0.2680747430608774, 0.2289319869095275, 0.22086131381677962, 0.12308775665262163, 0.5025676910983478, 2.462395878318936, 3.728271246727591, 3.2178174212105457, 2.309455809942361, 1.3865359038147909, 0.5466223127579335, 5.017547521429644, 4.974000223747219, 4.88991542918967, 4.759514021167544, 4.593184810574916, 4.373904367867737, 4.121678318076994, 3.77443412192461, 3.3272451234530562, 2.34359836277374, 0.8991145597217977, 0.3787548526682735, 0.4092565445648526, 0.3315260838843769, 0.3012627976055486, 0.26220542956020343, 0.2238678415518097, 0.21734873613471475, 0.1192764921471491, 0.49773011669650935, 2.457601114780113, 3.720845709186352, 3.209713116839522, 2.3023710558469817, 1.3810838201915885, 0.5444833667552511, 4.768672084056628, 4.728363221752855, 4.649785803304432, 4.529026803248024, 4.373904367867696, 4.17029454419516, 3.935471335597916, 3.610839056908706, 3.188636552448717, 2.250185425485392, 0.8732964981385812, 0.37549418044849747, 0.40499973555876145, 0.33089353293263624, 0.30185714836599853, 0.2641223216613046, 0.22665803192729536, 0.21995589874284244, 0.12349153427973876, 0.5027035340702964, 2.453262311888249, 3.7125378791919967, 3.1998349112472475, 2.292349229583595, 1.3739298269454523, 0.541129629176412, 4.482035392396979, 4.445101903956539, 4.3734524320812085, 4.2629329820960375, 4.121678318076912, 3.9354713355978697, 3.722412627570992, 3.423534266409342, 3.035103288048521, 2.1490518513422137, 0.8263465612381493, 0.3525212343319214, 0.3840337619639082, 0.3147007787982595, 0.2883391062246433, 0.2538800087383958, 0.2175047247681215, 0.21373677692975357, 0.11566406117311587, 0.4933483724752452, 2.450510832101593, 3.704806703548466, 3.187290030935986, 2.279466443398246, 1.363477163939125, 0.537241374925926, 4.092177812978943, 4.059698527708683, 3.9962079576459844, 3.8989230086417535, 3.7744341219244917, 3.6108390569086235, 3.4235342664093067, 3.1642735103527064, 2.8164401944541297, 2.004459351259045, 0.7979577756166729, 0.36176534213047806, 0.3889352989228144, 0.32585721198948436, 0.29937288708536863, 0.26634519859031724, 0.2304214702616582, 0.2243575715948639, 0.13028542415549915, 0.5107511485155931, 2.4515746805267695, 3.699952846442793, 3.172891179665464, 2.259981408469254, 1.3509288597766205, 0.5312210370734163, 3.5944469496490266, 3.5665271342665616, 3.5137731690095673, 3.4306099408369137, 3.3272451234529155, 3.1886365524486076, 3.035103288048452, 2.8164401944540955, 2.54984427106432, 1.8369739713524056, 0.6988076489707584, 0.2940588465477151, 0.33077160901510605, 0.2745823234824511, 0.25451381231073217, 0.2277368355916696, 0.19517998071087903, 0.19691849954266125, 0.09216019741352657, 0.4780890756353854, 2.471039635736939, 3.708446389454005, 3.1464427928749155, 2.236896343897969, 1.332760763460463, 0.5245168359451597, 2.523902686305217, 2.5050284886820773, 2.4692657980425863, 2.4130472881196994, 2.343598362773647, 2.2501854254853204, 2.1490518513421724, 2.004459351259023, 1.8369739713524011, 1.4335435554580034, 0.7607204734537925, 0.5438317077100563, 0.5559104200150047, 0.4982101974890649, 0.46035072999020127, 0.4215739885870017, 0.37177877115645996, 0.3626017581973225, 0.2760630999983546, 0.669572390584279, 2.580603040100902, 3.7047200828329143, 3.1118522186707125, 2.205285779832711, 1.3099064730683507, 0.515235793314731, 0.9669822247519037, 0.9610656476260654, 0.946103731875629, 0.9290695339819859, 0.8991145597217822, 0.8732964981385789, 0.8263465612381561, 0.797957775616672, 0.6988076489707739, 0.760720473453837, 1.1524086371366944, 1.2870856844129992, 1.2239792474435593, 1.1589358413233413, 1.0636892452350668, 0.9821711416390791, 0.890180951098714, 0.8288702538940438, 0.8086244363527214, 1.2390084011679154, 2.7648457236943664, 3.670437777639684, 3.071678544998882, 2.159553545660886, 1.2842109348019637, 0.5010986933196809, 0.403902129277409, 0.4024410803751159, 0.3959263031267219, 0.39220377577345833, 0.37875485266816034, 0.37549418044839167, 0.35252123433180915, 0.36176534213037037, 0.29405884654764913, 0.5438317077100766, 1.287085684412951, 1.6242107013132827, 1.5768817958798131, 1.5059259196175838, 1.394095101065989, 1.292072883155068, 1.1794797127802303, 1.1027696785709913, 1.1095609952437697, 1.5286635553469303, 2.8808939768778496, 3.6269616956325748, 3.0082071157050727, 2.1058951310001666, 1.2495727127267933, 0.48625679149685724, 0.43440683664377255, 0.43280015783761083, 0.4263929561489333, 0.42225669284758, 0.409256544564733, 0.4049997355586355, 0.3840337619637513, 0.38893529892267076, 0.3307716090150344, 0.5559104200150118, 1.2239792474434825, 1.57688179587971, 1.5822036493779645, 1.52402567656049, 1.4248243822920061, 1.3278470793729078, 1.2191936390090217, 1.1505255269367118, 1.1492717371979704, 1.5523048673844702, 2.8790342694444426, 3.562697375447255, 2.9219284040426228, 2.0406252215442846, 1.2069470667062705, 0.46971286812671875, 0.3485247128318029, 0.34755077416394725, 0.3430604843988394, 0.34085529258360303, 0.33152608388427285, 0.33089353293252266, 0.31470077879811864, 0.3258572119893694, 0.2745823234823962, 0.4982101974890858, 1.1589358413233333, 1.5059259196175045, 1.524025676560444, 1.486656639504871, 1.3987075073314899, 1.3111458418329234, 1.2107471245117176, 1.1434972818643057, 1.144467539725511, 1.5384232738777928, 2.8082830917511448, 3.454255977002327, 2.8172007855480756, 1.959687224413772, 1.1575795277135608, 0.4498412866972196, 0.3151404294484175, 0.31456669772971957, 0.31053080349236717, 0.3094169121097281, 0.30126279760547714, 0.3018571483659038, 0.2883391062245268, 0.29937288708529547, 0.25451381231070846, 0.460350729990248, 1.0636892452350764, 1.3940951010658849, 1.424824382291963, 1.3987075073315454, 1.325644358311717, 1.2491066157964286, 1.1573019529754685, 1.0974110818272127, 1.0982971346808643, 1.4739711189839857, 2.6958257144715456, 3.306862649836722, 2.6887479072060856, 1.865606309343153, 1.0999276107379026, 0.4273601354249974, 0.2715313622752205, 0.2712408323863486, 0.2683706660759315, 0.26807474306079393, 0.2622054295601173, 0.2641223216611936, 0.2538800087382719, 0.26634519859024375, 0.22773683559163585, 0.42157398858703904, 0.9821711416390954, 1.2920728831549482, 1.327847079372876, 1.311145841833025, 1.249106615796461, 1.1815683901227005, 1.0988147388968696, 1.0433414336034266, 1.046423028773479, 1.4038101451972587, 2.55280038900135, 3.126588522049194, 2.537847770235973, 1.7572833427842656, 1.035103411198167, 0.4016993817101232, 0.2311192663199795, 0.23104207019959092, 0.2286137817583847, 0.2289319869094536, 0.2238678415517248, 0.22665803192720455, 0.21750472476803354, 0.2304214702616034, 0.19517998071085046, 0.3717787711564949, 0.8901809510987333, 1.179479712780171, 1.2191936390090004, 1.2107471245117676, 1.1573019529754933, 1.0988147388968734, 1.0241776843697012, 0.9753716830843445, 0.9785371157959937, 1.3119982128975098, 2.389861787391721, 2.9224880894739855, 2.3670990773075857, 1.637024881102955, 0.9628214197233405, 0.37412087640897174, 0.2220817966840943, 0.22208236379263677, 0.2203897961602755, 0.22086131381671079, 0.2173487361346297, 0.2199558987427694, 0.21373677692969617, 0.22435757159482853, 0.19691849954264193, 0.36260175819736656, 0.828870253894074, 1.1027696785709717, 1.1505255269366674, 1.1434972818642755, 1.0974110818272036, 1.043341433603415, 0.9753716830843304, 0.9281934610624979, 0.9310769111007061, 1.238688471057421, 2.2233227993851052, 2.7033987213985453, 2.181431373698894, 1.5042912144490657, 0.88558197296699, 0.343658154095491, 0.12299711149256035, 0.12335175265850824, 0.12161488522087767, 0.12308775665254194, 0.11927649214707232, 0.12349153427967527, 0.1156640611730616, 0.13028542415547345, 0.09216019741350918, 0.2760630999984001, 0.8086244363527421, 1.1095609952437284, 1.1492717371979282, 1.1444675397255097, 1.0982971346808819, 1.0464230287734877, 0.9785371157959968, 0.9310769111007193, 0.9242175845445468, 1.1975380280431727, 2.088833975266839, 2.486071127739906, 1.9803672161076373, 1.3651090815695452, 0.80358304989205, 0.312069295998247, 0.503109112189356, 0.5033862627665521, 0.5011115173695708, 0.5025676910981631, 0.49773011669633227, 0.5027035340700841, 0.49334837247502555, 0.510751148515488, 0.47808907563538633, 0.669572390584326, 1.2390084011678888, 1.528663555346789, 1.552304867384417, 1.5384232738778985, 1.4739711189840574, 1.4038101451973033, 1.3119982128975423, 1.238688471057436, 1.1975380280431982, 1.3987826657791949, 2.0566292090818687, 2.2590747335471404, 1.7706180152946898, 1.2214691985593102, 0.718215334523856, 0.2796458430895011, 2.471489308913716, 2.46981152747386, 2.466561423208908, 2.4623958783186155, 2.457601114779793, 2.453262311887927, 2.450510832101404, 2.4515746805266367, 2.471039635736844, 2.580603040100968, 2.7648457236944672, 2.8808939768777693, 2.879034269444383, 2.8082830917512935, 2.695825714471705, 2.552800389001535, 2.3898617873918746, 2.2233227993851936, 2.088833975266921, 2.0566292090819274, 2.097575284497796, 1.930867536269584, 1.499447108015804, 1.0253507376374342, 0.6082027704198754, 0.2339841111979361, 3.7416525496826605, 3.7391992854430045, 3.7347546667150806, 3.728271246727024, 3.7208457091858467, 3.712537879191615, 3.7048067035482832, 3.6999528464426117, 3.708446389453743, 3.7047200828327576, 3.6704377776396644, 3.626961695632491, 3.5626973754471, 3.454255977002229, 3.3068626498366442, 3.126588522049113, 2.9224880894739056, 2.703398721398474, 2.486071127739863, 2.2590747335471053, 1.9308675362695422, 1.5391217934121573, 1.162334472441772, 0.7939648840242541, 0.4723682660858627, 0.18194651476246185, 3.2298487314462077, 3.2278575681256676, 3.223688846539704, 3.21781742120986, 3.2097131168389397, 3.1998349112467817, 3.187290030935613, 3.172891179665152, 3.1464427928746117, 3.111852218670406, 3.0716785449986075, 3.0082071157048107, 2.9219284040423616, 2.8172007855477945, 2.6887479072057614, 2.5378477702356093, 2.367099077307253, 2.18143137369863, 1.9803672161074484, 1.7706180152945494, 1.4994471080157148, 1.1623344724417508, 0.8530522072377981, 0.5840088694949934, 0.34853439454001545, 0.1350009611747798, 2.3196211054563376, 2.317937511775621, 2.3147261952794334, 2.309455809941834, 2.3023710558465074, 2.292349229583173, 2.2794664433978786, 2.2599814084689274, 2.236896343897682, 2.205285779832446, 2.159553545660636, 2.105895130999928, 2.0406252215440603, 1.9596872244135484, 1.8656063093429323, 1.7572833427840546, 1.6370248811027617, 1.504291214448897, 1.3651090815694091, 1.2214691985591957, 1.0253507376373534, 0.7939648840242249, 0.584008869494984, 0.398247139710676, 0.23975260736271592, 0.09284222302485375, 1.3935401763824353, 1.392476235030373, 1.390069672513636, 1.3865359038144307, 1.381083820191254, 1.3739298269451494, 1.363477163938854, 1.3509288597763736, 1.3327607634602323, 1.3099064730681402, 1.284210934801776, 1.2495727127266203, 1.2069470667061033, 1.1575795277134018, 1.0999276107377556, 1.0351034111980313, 0.9628214197232156, 0.8855819729668807, 0.8035830498919615, 0.7182153345237794, 0.6082027704198212, 0.472368266085839, 0.3485343945400058, 0.2397526073627135, 0.1442347378227854, 0.05646182371529659, 0.5497551443386562, 0.5492241381106334, 0.5483331806847328, 0.5466223127577606, 0.5444833667550928, 0.5411296291762662, 0.5372413749257926, 0.5312210370732945, 0.5245168359450487, 0.5152357933146287, 0.5010986933195894, 0.48625679149677564, 0.4697128681266468, 0.44984128669715456, 0.4273601354249342, 0.4016993817100624, 0.3741208764089195, 0.3436581540954487, 0.3120692959982139, 0.27964584308947227, 0.23398411119791424, 0.18194651476245274, 0.1350009611747764, 0.0928422230248525, 0.056461823715296316, 0.021905924441733903]]]

        phi_test = np.array(phi_test)

        keff_test = 1.07755031

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        l = 0
        phi = pydgm.state.mg_phi[l, :, :].flatten()
        phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
        np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()

    def test_solver_partisn_eigen_2g_l0_full(self):
        '''
        Test eigenvalue source problem 
        '''

        # Set the variables for the test
        self.set_eigen()
        self.set_mesh('c5g7')
        pydgm.control.scatter_leg_order = 0

        # Initialize the dependancies
        pydgm.dgmsolver.initialize_dgmsolver()

        assert(pydgm.control.number_groups == 2)

        # Solve the problem
        pydgm.dgmsolver.dgmsolve()

        # Partisn output flux indexed as group, Legendre, cell
        phi_test = [[[49.25620577737842, 48.699968781083825, 47.591452492774664, 45.94223786523866, 43.76257254042213, 41.079372511718, 37.90067305181414, 34.30662887230619, 30.257422046161476, 26.43233140887898, 22.804305300403897, 18.660266567252393, 15.089048378642676, 12.41693720444892, 10.203494291815293, 8.459250199887169, 7.070599757449037, 5.930446719292539, 5.133162208039793, 4.372866696682594, 2.6757824402733417, 1.1356814926401295, 0.5331212710522321, 0.2258914925445413, 0.10548029494329372, 0.03151792166162671, 48.69996878108384, 48.151136048182956, 47.05915136780214, 45.43136622718847, 43.283388591713866, 40.63693009179989, 37.5008616261787, 33.953627554429715, 29.957997369649274, 26.182517661186818, 22.599796781545088, 18.506110405994317, 14.978021110472307, 12.337763451816263, 10.148683155223168, 8.423913658008363, 7.049878008123343, 5.919370088768897, 5.128829058505758, 4.372226028834188, 2.6771983230251797, 1.1371700472180593, 0.5336318530515181, 0.22658499567466003, 0.10552005343394263, 0.03165374082937694, 47.591452492774685, 47.059151367802116, 45.99595674966689, 44.41711421813625, 42.326675202785076, 39.75438672601363, 36.70507664977021, 33.25506630928836, 29.361089064240637, 25.684383700024135, 22.19817462193938, 18.203724549204214, 14.759523255117603, 12.182550313747399, 10.046440146190202, 8.358325606003076, 7.011144411065795, 5.90034545800942, 5.122924864708136, 4.374740903694979, 2.680721658555908, 1.139876380967714, 0.5360914780685127, 0.22690489817300855, 0.1060900940282491, 0.031608289119473575, 45.94223786523865, 45.43136622718847, 44.41711421813625, 42.902436103371414, 40.905487641990725, 38.44228786875978, 35.52039763188368, 32.212269807424356, 28.478984930863888, 24.95199250494662, 21.60135403703289, 17.75851320485058, 14.443519529109912, 11.96265838544084, 9.898853899153739, 8.267471071372256, 6.962162122599054, 5.878363235940175, 5.119161729163283, 4.379856227557218, 2.6892107474462597, 1.1458257796184916, 0.5380714123620214, 0.22872740303427747, 0.10632666885010714, 0.031936346639397734, 43.762572540422084, 43.28338859171386, 42.32667520278508, 40.9054876419907, 39.02367178584013, 36.70733736294374, 33.95850013708625, 30.84217407979083, 27.31460579990725, 23.987726625981463, 20.83554495053807, 17.193166297065694, 14.04588650684601, 11.69030235765044, 9.729147011926333, 8.168961062780058, 6.913647189925698, 5.864650630783361, 5.127801957138629, 4.400860721219092, 2.704533798340448, 1.153503382610054, 0.5432090298612345, 0.22973469475937738, 0.10716298523305645, 0.03183039040018817, 41.07937251171795, 40.63693009179985, 39.75438672601361, 38.442287868759756, 36.70733736294371, 34.57021074772007, 32.032673425098295, 29.15656577981603, 25.896930665370082, 22.8233896230959, 19.89844832908882, 16.50967168945614, 13.580662610217685, 11.384093342582077, 9.543690183742909, 8.0708988503363, 6.877467318361588, 5.866703952249323, 5.1513628843413475, 4.43218520709538, 2.7317211411456643, 1.166968431738685, 0.5475772579869298, 0.23177419682120595, 0.10758598859701828, 0.03225242122701257, 37.90067305181403, 37.50086162617862, 36.70507664977015, 35.52039763188364, 33.958500137086226, 32.032673425098274, 29.749035531673265, 27.160963277355027, 24.216401403017855, 21.45621852474937, 18.85092474242547, 15.7753317209394, 13.098665164320149, 11.09019417440123, 9.391211885082862, 8.015548028495559, 6.887820833381089, 5.91344067691308, 5.219697515521666, 4.5061535003438875, 2.7729893049009897, 1.1820746550150631, 0.5538067801314122, 0.23307454179026366, 0.10850768437801343, 0.03229366387385039, 34.30662887230609, 33.95362755442961, 33.25506630928826, 32.212269807424285, 30.842174079790773, 29.156565779815995, 27.16096327735499, 24.90547844559236, 22.34270714743124, 19.946405503579964, 17.66337144358808, 14.952288593515863, 12.589169117529172, 10.80108348402798, 9.262918314904264, 7.995149611632287, 6.936258328034852, 5.996435051259984, 5.314095666397686, 4.588863105660319, 2.831563029101618, 1.201365804888352, 0.5577054844322771, 0.23528567026653047, 0.1085606700055352, 0.0325863514727874, 30.25742204616134, 29.95799736964914, 29.36108906424051, 28.478984930863763, 27.314605799907167, 25.89693066537, 24.21640140301782, 22.342707147431234, 20.20384388524381, 18.26596222629993, 16.493627092850925, 14.254966261465208, 12.243033384222556, 10.690095569733174, 9.310134788645115, 8.143565859611135, 7.141468198271729, 6.222217313601046, 5.53568103333491, 4.781848325449717, 2.910743245826567, 1.208109543907247, 0.5645033276926413, 0.23466588893039342, 0.11010191190923838, 0.03134326920525362, 26.43233140887881, 26.182517661186655, 25.684383700023965, 24.951992504946478, 23.987726625981338, 22.82338962309582, 21.456218524749307, 19.946405503579932, 18.265962226299923, 16.68860436501666, 15.26289155069099, 13.537119715932093, 11.947978026473452, 10.628064219614025, 9.420689576675237, 8.351765268518907, 7.402832711217428, 6.505262247108529, 5.797696207936393, 4.951632897567441, 2.94531656633827, 1.2133634520012804, 0.5686712052636744, 0.2337846485771993, 0.1105447042519855, 0.030753429328767182, 22.80430530040372, 22.599796781544892, 22.198174621939213, 21.601354037032735, 20.835544950537955, 19.898448329088733, 18.85092474242541, 17.66337144358804, 16.493627092850904, 15.262891550690993, 13.740571436431233, 12.438460196358049, 11.334036500048057, 10.253642842524641, 9.25659793377704, 8.308502312654772, 7.4351127650842725, 6.592535277033232, 5.846613772081663, 4.831313454148552, 2.912118838563383, 1.2315161241859884, 0.5596810662471193, 0.23760065365653593, 0.10638842021856719, 0.03334885546996396, 18.660266567252172, 18.506110405994107, 18.203724549204026, 17.75851320485041, 17.193166297065552, 16.50967168945604, 15.77533172093935, 14.95228859351583, 14.25496626146519, 13.537119715932086, 12.438460196358058, 11.500611832474275, 10.752744047945752, 9.914574018406766, 9.092075859335871, 8.262644365173347, 7.457520249536222, 6.659673729666697, 5.8854691603244556, 4.805247885594159, 2.8786589546899863, 1.2281585730039466, 0.5538563971988476, 0.23555488328351307, 0.10446144778944902, 0.033118086222752925, 15.08904837864248, 14.978021110472099, 14.759523255117402, 14.443519529109762, 14.045886506845902, 13.580662610217605, 13.098665164320103, 12.589169117529153, 12.243033384222562, 11.947978026473471, 11.334036500048086, 10.752744047945777, 10.258458968500582, 9.62869223752457, 8.947652801103839, 8.221934118898384, 7.481296034188097, 6.713258039401239, 5.94849987997485, 4.857450455668348, 2.8663064634553566, 1.2033476080396839, 0.5476299114761285, 0.22878754020585818, 0.10349385540178246, 0.031159732059927062, 12.416937204448653, 12.337763451816057, 12.18255031374724, 11.96265838544071, 11.690302357650337, 11.384093342582007, 11.090194174401214, 10.801083484027995, 10.690095569733206, 10.62806421961408, 10.253642842524705, 9.914574018406825, 9.628692237524607, 9.171931266895578, 8.62788993146506, 8.004275244654908, 7.334695859239677, 6.614124239558094, 5.873552504638985, 4.787284147639341, 2.8235912566926396, 1.1749066150345497, 0.5316425497271848, 0.22207500615874853, 0.09996208417287931, 0.029942827428576596, 10.203494291815273, 10.148683155223084, 10.046440146190077, 9.898853899153664, 9.729147011926324, 9.543690183742953, 9.391211885082951, 9.262918314904363, 9.31013478864523, 9.42068957667535, 9.25659793377715, 9.092075859335981, 8.947652801103924, 8.627889931465115, 8.196232635428744, 7.663925241388122, 7.068081287580334, 6.398132502652477, 5.6975317713847184, 4.652367034452571, 2.7341973179109704, 1.1328949733076377, 0.5103885716506276, 0.21221968310495307, 0.0953173093593201, 0.028693479732356152, 8.45925019988685, 8.42391365800816, 8.358325606003007, 8.267471071372245, 8.168961062780072, 8.070898850336366, 8.01554802849565, 7.995149611632408, 8.14356585961129, 8.351765268519083, 8.308502312654962, 8.262644365173522, 8.221934118898528, 8.004275244655021, 7.663925241388174, 7.213190501822295, 6.6863325100768725, 6.075245293925045, 5.419363739639009, 4.425654385817577, 2.603357994621526, 1.0747973387108452, 0.4807603176321027, 0.1998541801947904, 0.08956823949467937, 0.027229827393764332, 7.070599757449896, 7.04987800812392, 7.0111444110661605, 6.962162122599447, 6.913647189926164, 6.8774673183620685, 6.8878208333815705, 6.936258328035284, 7.141468198272111, 7.402832711217767, 7.435112765084541, 7.4575202495364525, 7.481296034188309, 7.334695859239842, 7.068081287580443, 6.686332510076923, 6.221283386032149, 5.6673431256384195, 5.064735889750218, 4.138729481718069, 2.425878346501698, 0.9956222192838778, 0.4452148638073639, 0.18375032700132007, 0.08343526381143777, 0.02473075408764186, 5.930446719291461, 5.919370088768407, 5.900345458009583, 5.8783632359405, 5.864650630783595, 5.866703952249464, 5.913440676913203, 5.996435051260151, 6.222217313601299, 6.5052622471089165, 6.592535277033625, 6.6596737296670225, 6.713258039401519, 6.614124239558303, 6.398132502652632, 6.07524529392514, 5.667343125638461, 5.173514653235359, 4.624299166062046, 3.771724204081838, 2.204699337812874, 0.8962883399861955, 0.3996078853415585, 0.16712965150065406, 0.07517338012185967, 0.022772450468546018, 5.133162208037961, 5.128829058505214, 5.122924864708481, 5.119161729163712, 5.127801957138917, 5.1513628843414745, 5.219697515521719, 5.314095666397729, 5.535681033335135, 5.79769620793692, 5.846613772082241, 5.885469160324882, 5.948499879975162, 5.873552504639213, 5.697531771384894, 5.419363739639134, 5.06473588975029, 4.624299166062078, 4.136283251175828, 3.3631542526290437, 1.9260473457844443, 0.769715216259445, 0.3516554248909138, 0.14646302826938581, 0.06755694383083143, 0.019867537273142468, 4.372866696686904, 4.3722260288373525, 4.374740903696687, 4.379856227558727, 4.40086072122082, 4.432185207096997, 4.506153500345392, 4.588863105661428, 4.781848325450616, 4.9516328975682, 4.8313134541490514, 4.805247885594532, 4.8574504556686255, 4.787284147639542, 4.652367034452738, 4.425654385817696, 4.138729481718149, 3.77172420408188, 3.363154252629059, 2.717386847363744, 1.5499626123140606, 0.635383770687322, 0.2991675859594647, 0.12544126248347678, 0.059077959558039635, 0.017180014443239473, 2.675782440275578, 2.677198323026849, 2.680721658557113, 2.689210747447201, 2.704533798341395, 2.7317211411465894, 2.77298930490183, 2.831563029102334, 2.910743245827121, 2.9453165663386347, 2.9121188385636394, 2.8786589546902004, 2.8663064634555258, 2.823591256692771, 2.734197317911075, 2.6033579946216014, 2.4258783465017486, 2.2046993378129054, 1.9260473457844596, 1.5499626123140662, 0.9918241219380423, 0.47582359092592197, 0.22179843667053795, 0.10214224907923698, 0.04496881232158825, 0.01597682805488567, 1.1356814926394736, 1.137170047217885, 1.1398763809680181, 1.1458257796187903, 1.1535033826101877, 1.1669684317387468, 1.1820746550151016, 1.2013658048884361, 1.2081095439073533, 1.2133634520013914, 1.2315161241861197, 1.2281585730040605, 1.203347608039775, 1.1749066150346221, 1.1328949733076923, 1.0747973387108858, 0.9956222192839067, 0.8962883399862158, 0.7697152162594578, 0.6353837706873304, 0.4758235909259253, 0.2845017512628703, 0.14382706491633612, 0.07041143872144441, 0.03195333527353333, 0.01173509432724924, 0.5331212710525798, 0.5336318530517845, 0.5360914780686942, 0.538071412362233, 0.5432090298614586, 0.5475772579871225, 0.5538067801315834, 0.5577054844324103, 0.564503327692751, 0.5686712052637679, 0.5596810662471853, 0.5538563971988991, 0.547629911476173, 0.5316425497272206, 0.5103885716506552, 0.48076031763212396, 0.44521486380737946, 0.3996078853415694, 0.3516554248909216, 0.2991675859594697, 0.22179843667054092, 0.14382706491633693, 0.08502524447108209, 0.04392223772382694, 0.021420152918392523, 0.007671473104903386, 0.225891492544328, 0.22658499567453486, 0.22690489817298584, 0.22872740303427147, 0.22973469475936925, 0.23177419682120015, 0.23307454179025067, 0.23528567026652816, 0.23466588893040025, 0.23378464857721426, 0.23760065365656377, 0.23555488328353952, 0.22878754020587885, 0.2220750061587663, 0.21221968310496678, 0.19985418019480086, 0.18375032700132815, 0.16712965150065995, 0.14646302826938976, 0.12544126248347984, 0.10214224907923862, 0.07041143872144516, 0.04392223772382712, 0.025572711511439288, 0.012718132261179979, 0.004916629812839443, 0.10548029494341978, 0.10552005343401182, 0.10609009402825861, 0.10632666885012697, 0.10716298523309502, 0.10758598859705962, 0.10850768437805872, 0.10856067000556875, 0.11010191190926073, 0.11054470425200223, 0.10638842021857549, 0.1044614477894579, 0.10349385540179219, 0.09996208417288675, 0.09531730935932684, 0.08956823949468433, 0.08343526381144155, 0.07517338012186243, 0.06755694383083359, 0.05907795955804096, 0.044968812321589266, 0.031953335273533716, 0.021420152918392707, 0.01271813226118003, 0.007146827204802524, 0.0025655585222951758, 0.031517921661524236, 0.031653740829328106, 0.0316082891194765, 0.031936346639387964, 0.03183039040016434, 0.03225242122699254, 0.032293663873831285, 0.03258635147277958, 0.03134326920525016, 0.030753429328765437, 0.03334885546996899, 0.0331180862227558, 0.03115973205992914, 0.029942827428579104, 0.028693479732358064, 0.027229827393766382, 0.024730754087643147, 0.022772450468547267, 0.019867537273143162, 0.017180014443240164, 0.01597682805488598, 0.011735094327249444, 0.007671473104903445, 0.004916629812839455, 0.0025655585222951983, 0.0012943638207216902]], [[7.333262373838789, 7.24976070507084, 7.086252882915231, 6.83797059967648, 6.517722450383744, 6.109774165778744, 5.643763476166613, 5.057929370219978, 4.362099552710367, 2.941635321641731, 1.0185493280578732, 0.38682872063043516, 0.42712663579703103, 0.31040164128346537, 0.27315562394647075, 0.2192177123614533, 0.1815303884800926, 0.16810547284958977, 0.08702805814114514, 0.3205927000928098, 1.6172666045814341, 2.2574663136570696, 1.6535436347141041, 1.0115367621400453, 0.5236117629317164, 0.18488376165588882, 7.249760705070843, 7.16761400237371, 7.00608648307782, 6.761682495433065, 6.445558392510209, 6.043415710334613, 5.583715500957926, 5.00563875659682, 4.318009938064057, 2.912805976265821, 1.0099584364994243, 0.38463829164946844, 0.4246362979861385, 0.3090694988728574, 0.27230093805336075, 0.21887058433372641, 0.18143542463033296, 0.16823076442865642, 0.08732835265125288, 0.321351559812034, 1.6191346058628364, 2.260593142219062, 1.656380312736779, 1.0132940076498438, 0.5245730575126958, 0.18514866631409457, 7.0862528829152325, 7.00608648307782, 6.849715603735813, 6.6113915056729935, 6.304806412289426, 5.913325450882641, 5.466312550678042, 4.903059482139335, 4.2331848795970695, 2.8574020579655546, 0.9896887480830379, 0.37683080153538906, 0.41670678285808127, 0.30404852780750286, 0.26804590153596597, 0.21617282909587376, 0.1792825964983495, 0.1670153233476076, 0.08602306980904656, 0.32071987953058956, 1.6232336281593052, 2.2675697896030576, 1.6620740868895483, 1.0170190162055708, 0.5262897763778691, 0.18584424065047245, 6.837970599676479, 6.761682495433058, 6.611391505672994, 6.38433809592049, 6.090194752202758, 5.715998823555208, 5.2879084094931725, 4.747766817023842, 4.1028129078308355, 2.77225215898413, 0.9649874364891344, 0.3710883776661027, 0.4100968200738359, 0.3009196552582619, 0.2662127916621532, 0.21582891874675564, 0.17962085688287874, 0.16794034674980513, 0.08733729902813273, 0.3237565601343245, 1.6306594939079708, 2.2789867357431914, 1.6713332632435265, 1.0223939618840228, 0.5290179919295273, 0.186597121578367, 6.517722450383738, 6.445558392510203, 6.304806412289422, 6.090194752202759, 5.814318118072564, 5.461316091225555, 5.058470563563553, 4.548080396924937, 3.9381109430111034, 2.665507850528608, 0.9250493261656364, 0.3553181672770947, 0.394443606924904, 0.2908625869469541, 0.2579582710211293, 0.21058467101393824, 0.17539689963027785, 0.16564933565723286, 0.08458628720412112, 0.322691051689391, 1.642364991704561, 2.2965173898320166, 1.6840507268838092, 1.0297786537774516, 0.5321401340850317, 0.18780294317947208, 6.109774165778736, 6.04341571033461, 5.913325450882634, 5.715998823555206, 5.461316091225559, 5.136425956793815, 4.764933532008966, 4.29338427106663, 3.725796061766216, 2.5273913620097317, 0.8879373069862259, 0.34946802063694526, 0.38684793530411654, 0.28933924898969404, 0.2579256383261498, 0.21292214083692465, 0.17854776344833884, 0.16935622041048728, 0.08859381761077029, 0.33067654711963756, 1.659943212406681, 2.320942970208728, 1.7008510859859352, 1.0382815211728469, 0.5359898188807103, 0.1887898254035285, 5.643763476166602, 5.5837155009579105, 5.466312550678032, 5.287908409493168, 5.058470563563547, 4.764933532008966, 4.431468576929856, 4.003769170951097, 3.489794464711225, 2.37692685888481, 0.8275945396687722, 0.32307735701187307, 0.36250847069850684, 0.2725814619968444, 0.24482018434733116, 0.20410533004744968, 0.17117905442470194, 0.16535925471680993, 0.08278097207971756, 0.32795023905333975, 1.6848900926457435, 2.3536673486668644, 1.720778308809737, 1.0481398382658131, 0.539163221177371, 0.19028146177483166, 5.057929370219962, 5.005638756596805, 4.9030594821393265, 4.747766817023836, 4.5480803969249255, 4.293384271066626, 4.003769170951096, 3.636810582748333, 3.1846740998345093, 2.181444612169021, 0.789534382754777, 0.3328365214633062, 0.3666412244575284, 0.28577497409910224, 0.2578372311555282, 0.21949794362749667, 0.18644054071962027, 0.17930644709516166, 0.09764598208622201, 0.3499283571832986, 1.7185026553520795, 2.3954522896391572, 1.744542839552061, 1.0559040407542928, 0.5428932054239864, 0.19084524211692672, 4.362099552710346, 4.318009938064041, 4.2331848795970535, 4.102812907830816, 3.9381109430110905, 3.7257960617662063, 3.4897944647112182, 3.1846740998345053, 2.837561062382632, 1.9680738733910723, 0.6751885981092157, 0.2566065825359507, 0.3016146129778254, 0.2318732312617057, 0.21247226521120033, 0.18216964298510901, 0.15323702834145897, 0.15453843181828963, 0.06477172897779218, 0.326214291214278, 1.768691778413892, 2.4548498320861842, 1.762270837614142, 1.0641388234989124, 0.5441927713345742, 0.1917113323874802, 2.9416353216417215, 2.9128059762658087, 2.857402057965541, 2.7722521589841183, 2.6655078505285994, 2.5273913620097246, 2.3769268588848056, 2.181444612169017, 1.968073873391072, 1.4783138416747372, 0.7210291154302572, 0.48999667834085703, 0.498526310216771, 0.42891379493328835, 0.39037821848437354, 0.3487190417670467, 0.3026300321013409, 0.2906108412813759, 0.2052163733020795, 0.4823708509278251, 1.8991589745545838, 2.50721434786691, 1.776356221472282, 1.0688511334476969, 0.5433830598866906, 0.1916961446828566, 1.0185493280578632, 1.0099584364994159, 0.9896887480830306, 0.9649874364891279, 0.9250493261656314, 0.8879373069862213, 0.8275945396687693, 0.7895343827547748, 0.6751885981092146, 0.7210291154302567, 1.1201079319380567, 1.2471908588554421, 1.1536999599133362, 1.0702768527246904, 0.9648815683141786, 0.8776416720790119, 0.7826546359534444, 0.7122189678378065, 0.654314387442401, 0.9721162603187242, 2.101854471244784, 2.5321814405888015, 1.7895361072711309, 1.064055105026111, 0.542437782221731, 0.1883885328627738, 0.3868287206304344, 0.38463829164946617, 0.3768308015353862, 0.3710883776660997, 0.355318167277093, 0.34946802063694415, 0.32307735701187296, 0.3328365214633062, 0.25660658253595064, 0.4899966783408575, 1.2471908588554426, 1.5829019389094527, 1.5009643967925692, 1.4101328402844084, 1.288041007095991, 1.1792293392014888, 1.061458957344153, 0.9677128375981124, 0.9219998514922084, 1.2379639063306471, 2.244919941906508, 2.5502105116639, 1.784414710526266, 1.0550564540126524, 0.5359039111098527, 0.18529250849186013, 0.42712663579701704, 0.4246362979861273, 0.4167067828580729, 0.4100968200738291, 0.39444360692489805, 0.386847935304112, 0.36250847069850334, 0.36664122445752634, 0.3016146129778241, 0.49852631021677113, 1.1536999599133395, 1.500964396792573, 1.481927321103715, 1.4111120173580176, 1.3082886170361703, 1.2089145428657253, 1.0968838161283905, 1.0102303530582355, 0.9594350755453536, 1.2685860689269255, 2.280449692073481, 2.5506502694130546, 1.760072260409824, 1.0380994311427465, 0.5243467961850049, 0.18155544996413525, 0.31040164128347025, 0.3090694988728599, 0.30404852780750297, 0.30091965525826203, 0.2908625869469552, 0.28933924898969565, 0.2725814619968468, 0.28577497409910557, 0.23187323126170764, 0.42891379493329224, 1.0702768527246975, 1.4101328402844153, 1.4111120173580236, 1.368015345276815, 1.281599214738159, 1.1952599030588467, 1.0931613718331756, 1.0098125426672566, 0.9622198963081517, 1.2701696849564774, 2.254143405613813, 2.508748715712108, 1.7201320122913062, 1.008772945863207, 0.5087656231706115, 0.1756361430072785, 0.273155623946452, 0.27230093805334665, 0.2680459015359564, 0.266212791662146, 0.2579582710211235, 0.25792563832614573, 0.24482018434732827, 0.25783723115552754, 0.21247226521119975, 0.3903782184843768, 0.9648815683141903, 1.2880410070960053, 1.3082886170361818, 1.2815992147381678, 1.2142391488725628, 1.1414217378650917, 1.0499499764583393, 0.975079138077861, 0.9307298611969156, 1.2282342488618754, 2.1859739160044795, 2.4267559692298017, 1.657877385549784, 0.9689039026578702, 0.48719778882015796, 0.16826489204313674, 0.21921771236147522, 0.21887058433374212, 0.21617282909588398, 0.21582891874676524, 0.21058467101394812, 0.21292214083693525, 0.20410533004745998, 0.21949794362750666, 0.1821696429851159, 0.3487190417670575, 0.8776416720790318, 1.1792293392015123, 1.2089145428657464, 1.1952599030588622, 1.1414217378651, 1.0798295650594054, 0.998609528025471, 0.9300524101570444, 0.890227878423587, 1.175369943507706, 2.081652678217609, 2.3075476246197777, 1.5730528437664508, 0.9168466908877909, 0.46053067005301407, 0.15875258954364826, 0.18153038848004946, 0.18143542463030318, 0.1792825964983306, 0.1796208568828657, 0.17539689963026764, 0.17854776344833165, 0.17117905442469586, 0.18644054071961827, 0.1532370283414565, 0.3026300321013475, 0.7826546359534707, 1.0614589573441855, 1.0968838161284202, 1.093161371833199, 1.0499499764583546, 0.998609528025479, 0.9269111659651412, 0.8663159618359436, 0.8301534679003099, 1.0964395332904915, 1.9469569996729328, 2.1555688123871617, 1.4663027878653447, 0.8537653532913501, 0.42811279633382315, 0.14805187000203296, 0.16810547284959612, 0.1682307644286654, 0.16701532334761712, 0.16794034674982003, 0.16564933565724713, 0.16935622041049914, 0.1653592547168208, 0.1793064470951717, 0.1545384318182969, 0.2906108412813908, 0.712218967837841, 0.9677128375981607, 1.0102303530582806, 1.0098125426672908, 0.9750791380778855, 0.9300524101570594, 0.8663159618359513, 0.8098175837421265, 0.7766101424654334, 1.020524777728552, 1.7920512018290766, 1.9767885806777705, 1.3410702255746794, 0.7791399502040498, 0.3919912831911509, 0.13523967287077077, 0.08702805814065824, 0.0873283526509178, 0.08602306980884636, 0.0873372990279809, 0.08458628720397968, 0.08859381761063742, 0.08278097207959793, 0.09764598208612547, 0.06477172897772711, 0.20521637330205802, 0.6543143874424348, 0.9219998514922642, 0.9594350755454002, 0.9622198963081884, 0.930729861196941, 0.8902278784236044, 0.8301534679003211, 0.776610142465438, 0.7390287412280567, 0.9524414214790055, 1.6437546089730253, 1.7835562463188885, 1.196501227438943, 0.6979939674839413, 0.3517515061490933, 0.12167468923895108, 0.3205927000934062, 0.3213515598124799, 0.3207198795308331, 0.32375656013453835, 0.3226910516896023, 0.33067654711983047, 0.3279502390535243, 0.34992835718342863, 0.32621429121437767, 0.4823708509279181, 0.9721162603188357, 1.2379639063307506, 1.2685860689270039, 1.270169684956539, 1.2282342488619185, 1.1753699435077385, 1.0964395332905141, 1.0205247777285673, 0.9524414214790123, 1.0904358041176017, 1.5648330318366106, 1.5670544749429145, 1.0416378967921016, 0.6123375570144779, 0.30882713325245886, 0.10752024161913243, 1.6172666045849173, 1.619134605865201, 1.6232336281606763, 1.6306594939090693, 1.6423649917056171, 1.6599432124076847, 1.684890092646663, 1.718502655352815, 1.7686917784144185, 1.8991589745549378, 2.1018544712450233, 2.2449199419066956, 2.2804496920736286, 2.254143405613926, 2.185973916004568, 2.0816526782176754, 1.9469569996729803, 1.7920512018291093, 1.6437546089730442, 1.5648330318366193, 1.5043322410456619, 1.2504591326898324, 0.8416707372718781, 0.49325276675168167, 0.2542804990786605, 0.08639859166952789, 2.25746631365791, 2.2605931422199026, 2.2675697896038587, 2.2789867357438953, 2.2965173898326356, 2.3209429702092876, 2.353667348667365, 2.395452289639602, 2.454849832086571, 2.5072143478672357, 2.532181440589081, 2.5502105116641203, 2.5506502694132207, 2.5087487157122434, 2.4267559692299114, 2.307547624619863, 2.155568812387225, 1.9767885806778154, 1.783556246318918, 1.567054474942933, 1.2504591326898407, 0.8957074884843471, 0.5995230651685285, 0.3576039623834623, 0.18689591011161105, 0.06396087514942754, 1.653543634712024, 1.6563803127355874, 1.6620740868890982, 1.6713332632433286, 1.6840507268836244, 1.700851085985739, 1.720778308809567, 1.7445428395519689, 1.7622708376141603, 1.7763562214724073, 1.7895361072713134, 1.7844147105264299, 1.7600722604099535, 1.7201320122914183, 1.6578773855498758, 1.5730528437665245, 1.466302787865401, 1.3410702255747216, 1.1965012274389721, 1.0416378967921214, 0.8416707372718893, 0.5995230651685313, 0.3949476880129871, 0.24168220088636952, 0.12840574519017306, 0.044645385966682744, 1.011536762139562, 1.0132940076493482, 1.0170190162051829, 1.0223939618838225, 1.0297786537773717, 1.0382815211728136, 1.0481398382658078, 1.0559040407543132, 1.0641388234989566, 1.0688511334477586, 1.0640551050261817, 1.0550564540127287, 1.0380994311428224, 1.0087729458632761, 0.9689039026579283, 0.9168466908878391, 0.8537653532913873, 0.7791399502040776, 0.697993967483962, 0.6123375570144927, 0.493252766751691, 0.35760396238346626, 0.24168220088637057, 0.14916264548351757, 0.08164092977630992, 0.028439409802611924, 0.5236117629314165, 0.5245730575124061, 0.5262897763776269, 0.5290179919293552, 0.532140134084926, 0.5359898188806541, 0.539163221177343, 0.5428932054239806, 0.5441927713345847, 0.5433830598867063, 0.542437782221752, 0.5359039111098818, 0.5243467961850402, 0.5087656231706464, 0.4871977888201881, 0.4605306700530393, 0.42811279633384397, 0.3919912831911667, 0.35175150614910483, 0.30882713325246774, 0.25428049907866623, 0.1868959101116138, 0.1284057451901742, 0.08164092977631021, 0.0448517636700611, 0.01614422318963832, 0.18488376165565099, 0.18514866631394408, 0.1858442406503843, 0.18659712157829472, 0.18780294317940702, 0.18878982540347897, 0.19028146177480001, 0.1908452421169066, 0.19171133238746807, 0.19169614468285548, 0.18838853286277932, 0.18529250849186782, 0.18155544996414533, 0.17563614300728905, 0.16826489204314674, 0.15875258954365679, 0.14805187000203968, 0.13523967287077615, 0.12167468923895522, 0.1075202416191354, 0.08639859166952993, 0.06396087514942847, 0.04464538596668323, 0.02843940980261211, 0.016144223189638346, 0.0056152153537533545]]]

        phi_test = np.array(phi_test)

        keff_test = 1.10972327

        # Test the eigenvalue
        self.assertAlmostEqual(pydgm.state.keff, keff_test, 8)

        # Test the scalar flux
        for l in range(pydgm.control.scatter_leg_order + 1):
            with self.subTest(l=l):
                phi = pydgm.state.mg_phi[l, :, :].flatten()
                phi_zero_test = phi_test[:, l].flatten() / np.linalg.norm(phi_test[:, l]) * np.linalg.norm(phi)
                np.testing.assert_array_almost_equal(phi, phi_zero_test, 8)

        self.angular_test()


if __name__ == '__main__':

    unittest.main()
