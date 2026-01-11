# BB84 QKD Simulator - mini Project
# Shree G - Beginner Version
# Simulates quantum key distribution with noise and Eve spying!

import random

def bit_flip_prob(prob):
    """Simple noise function - flip bit with probability"""
    return random.random() < prob

def calculate_fidelity(alice_key, bob_key):
    """Check how many bits match - student style"""
    correct = 0
    total = len(alice_key)
    for i in range(total):
        if alice_key[i] == bob_key[i]:
            correct += 1
    return (correct / total) * 100

# Main BB84 Simulation
def bb84_student_simulator():
    print("🔬 BB84 QKD SIMULATION STARTING...")
    print("Channel noise: 10%, Eve attack probability: 5%")
    
    # Parameters 
    N_BITS = 1000  # Total qubits sent
    CHANNEL_NOISE = 0.10
    EVE_PROB = 0.05
    
    # Step 1: Alice creates random bits and bases
    print("\n1. Alice generating random bits and bases...")
    alice_bits = []
    alice_bases = []
    for i in range(N_BITS):
        alice_bits.append(random.randint(0,1))
        alice_bases.append(random.randint(0,1))  # 0=rectilinear, 1=diagonal
    print(f"Alice sent {N_BITS} qubits")
    
    # Step 2: Bob chooses random bases
    print("2. Bob choosing measurement bases...")
    bob_bases = []
    for i in range(N_BITS):
        bob_bases.append(random.randint(0,1))
    
    # Step 3: Transmission with NOISE + EVE
    print("3. Qubits traveling through noisy channel + Eve attack...")
    bob_measurements = alice_bits[:]  # Start with Alice's bits
    
    for i in range(N_BITS):
        # Channel noise - flip bits randomly
        if bit_flip_prob(CHANNEL_NOISE):
            bob_measurements[i] = 1 - bob_measurements[i]
        
        # Eve attack! (5% chance she intercepts)
        if bit_flip_prob(EVE_PROB):
            print(f"   Eve intercepted qubit {i}!")
            # Eve picks random basis
            eve_basis = random.randint(0,1)
            
            # Eve measures (simplified)
            if eve_basis == alice_bases[i]:
                eve_bit = alice_bits[i]
            else:
                eve_bit = random.randint(0,1)  # 50% error
            
            # Eve sends to Bob in her basis
            if bob_bases[i] == eve_basis:
                bob_measurements[i] = eve_bit
            else:
                bob_measurements[i] = random.randint(0,1)
    
    # Step 4: SIFTING - compare bases over phone
    print("\n4. SIFTING: Alice and Bob compare bases...")
    alice_key = []
    bob_key = []
    
    for i in range(N_BITS):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_measurements[i])
    
    print(f"Sifted key length: {len(alice_key)} bits (~{len(alice_key)/N_BITS*100:.0f}%)")
    
    # Step 5: Check QBER (error rate)
    fidelity_percent = calculate_fidelity(alice_key, bob_key)
    qber = 100 - fidelity_percent
    print(f"\n RESULTS:")
    print(f"Key Fidelity: {fidelity_percent:.1f}%")
    print(f"QBER (error): {qber:.1f}%")
    
    # Security check
    if qber > 11:
        print("EVE DETECTED! QBER too high - discard key!")
        final_key = "ABORTED"
    else:
        print("Key secure! Eve not detected.")
        # Show first 20 bits of final key
        final_key = ""
        for i in range(min(20, len(alice_key))):
            final_key += str(alice_key[i])
        print(f"Final key (first 20): {final_key}...")
    
    print("\n" + "="*50)
    return fidelity_percent, qber

# Run 10 simulations like a student would
print("BB84 SIMULATOR - 10 RUNS")
total_fidelity = 0
total_qber = 0

for run in range(10):
    print(f"\n--- Run {run+1}/10 ---")
    fid, qber_val = bb84_student_simulator()
    total_fidelity += fid
    total_qber += qber_val

print("\n FINAL AVERAGE RESULTS:")
print(f"Average Fidelity: {total_fidelity/10:.1f}% (Target: 95%)")
print(f"Average QBER: {total_qber/10:.1f}%")
