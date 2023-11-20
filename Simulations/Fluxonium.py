def hamiltonian(E_J1,E_J2,E_C,phi_e,N, phi_cutoff,charge_offset, k):
    # We make our phi matrix
    phi_array = np.linspace(-phi_cutoff, phi_cutoff, N)
    phi_matrix = np.diag(phi_array)
    # our delta
    delta = phi_array[2]-phi_array[1]
    # We make our n^2 matrix
    n2_matrix = ((-1) / (delta ** 2)) * (-2 * np.diag(np.ones(N )) + np.diag(np.ones(N-1), -1) + np.diag(np.ones(N-1), 1))
    n2_matrix[0, N-1] = 1
    n2_matrix[N-1, 0] = 1

    # Make a matrix with the chargeoffset in the diagonal
    n_chargeoffset = np.diag(charge_offset)

    # Make the n matrix
    n_matrix = ((-1j)/(2*delta)) * (-np.diag(np.ones(N-1), -1) + np.diag(np.ones(N-1), 1))
    n_matrix[0,N-1] = -1
    n_matrix[N-1,0] = 1

    # Define the capacitor term
    n = 2*n_chargeoffset*n_matrix
    Capacitor = (n2_matrix-n).multiply(4*E_C)

    # Calculate the Josephson term
    gamma = E_J2/E_J1
    d = (gamma-1)/(gamma+1)

    # Define new josephson energy
    E_J = (E_J1+E_J2)*np.sqrt(math.cos(phi_e)^2 +d^2* (math.sin(phi_e)^2)) 
    phi_matrix.data = np.cos(phi_matrix.data)
    JJ = phi_matrix.multiply(-E_J)

    # Define the hamiltonian
    Hamiltonian = Capacitor + JJ
    Hamiltonian = sp.csr_matrix(Hamiltonian)
    eig_vals, eig_vec = linalg.eigsh(Hamiltonian, k, which ="SM")
    w_q = eig_vals[1]-eig_vals[0]
    return np.array(phi_matrix), np.array(n_matrix.toarray()), Hamiltonian 
