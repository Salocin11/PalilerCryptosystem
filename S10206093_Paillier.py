import random

def main_menu():
    print("Paillier Cryptosystem. Done by Nicolas Teo. P06 S10206093")
    print("Welcome")
    print("The Paillier Cryptosystem is a public key cryptosystem with the property of homomorphic encryption which will be showcased in this code.")
    print("NOTE:")
    print("Please note that there is a very small chance that the code would produce false results. If that does happen please restart the code and key in the same values.")
    print("When choosing the plaintext to enter. Ensure that the value of plaintext is smaller than the value of N")
    print("This code only supports integers")
    print("Entering big plaintext values would cause python to miscalculate and thus cause the algorithim to fail")
    print("It is recommended to enter values smaller than 100")
    print("It has been noticed that the calculations for voting would sometimes glitch and produce false values")

def main():
    ########################### Key generation #######################
    n,g,lamda = key_generate()
    while mmi(lamda,g,n) == False:
        n,g,lamda = key_generate()
    print("\nKey Generation will now start.")
    print("The N value is: " + str(n))
    print("The g value is: " + str(g))
    print("The lamda value is: " + str(lamda))
    print("The Public key is ("+str(n)+", " + str(g) +")")
    print("The Private key is " + str(lamda))
    print("Key Generation has ended. \n")

    ########################### Encryption  ##########################
    print("Encryption of plaintext to be inputted can now begin.")
    c = encryption(n,g)
    ########################### Decryption  ##########################
    print("\nNow decryption of inputted plaintext will begin.")
    decryption(c,n,lamda,g)
    ########################### Homomorphic addition  ################
    Csum = HaddEncrypt(n,g,c)
    decryption(Csum,n,lamda,g)
    ########################### Homomorphic multiplication  ##########
    c3p = HmultiEncrypt(n,g,c)
    decryption(c3p,n,lamda,g)
    ########################### Voting  ##############################
    voting(n,g,lamda)
    
    
    
    
#Key Generation
def p_q_generate():
    p = random.randint(50,200)
    q = random.randint(50,200)
    while isPrime(p) == False or isPrime(q) == False or p==q:
        if isPrime(p) == False:
            p = random.randint(50,200)
        if isPrime(q) == False:
            q = random.randint(50,200)
    return p , q
    
def key_generate():
    p , q = p_q_generate()
    n = p*q
    while gcd(n,(p-1)*(q-1)) != 1:
        p , q = p_q_generate()
        n = p*q
    lamda = lcm(p-1,q-1)
    g = random.randint(1,n**2)
    while mmi(lamda,g,n) == False:
        print("If this message appears multiple time it means that Python has encountered a processing error as it has exceeded the total number of times that it can loop itself through the key generation function and has thus crashed. Please restart the program.")
        key_generate()
    return n,g,lamda
        
               
    


def mmi(lamda,g,n):
    try:
        k = ((Lfunc(g**lamda % n**2,n))**1) % n
        ans = pow(k,-1,n)
        ans += 1
        return True         #Does not exist
    except:
        return False


def encryption(n,g):
    m = int(input("Enter plaintext ( Eg: 12 )"))
    r = random.randint(1,n-1)
    c = g**m * r**n % n**2
    print("The encrypted value (C) of plaintext inputted is: "+str(c))
    return c

def decryption(c,n,lamda,g):
    k = ((Lfunc(g**lamda % n**2,n))**1) % n
    ans = pow(k,-1,n)
    plaintext = (Lfunc(c**lamda % n**2,n) * ans) % n
    print("Plaintext: " + str(plaintext))
def Lfunc(x,n):
    return((x-1)//n)
    
    

    
def gcd(a,b): 
    if(b==0): 
        return(a) 
    else: 
        return(gcd(b,a%b))

def lcm(x, y):
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1
   return lcm

def isPrime(n):
    if n <= 1 or n% 1 > 0:
        return False
    else:
        pass
    for i in range(2,n//2):
        
        if n% i ==0:
            return False
        else:
            pass
    return True

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcdi, x, y = egcd(b % a, a)
		return (gcdi, y - (b//a) * x, x)

# Homomorphic addition
def HaddEncrypt(n,g,c):
    print("\nThis showcases the Homomorphic property of Addition of two ciphertexts")
    print("When two ciphertexts are multiplied, the result decrypts to the sum of their plaintexts")
    m2 = int(input("Pls input plaintext value of cipher that u want to be added: "))
    r2 = random.randint(1,n-1)
    c2 = g**m2 * r2**n % n**2
    Csum = c * c2 
    print("Csum is " + str(Csum))
    return Csum

# Homomorphic multiplication
def HmultiEncrypt(n,g,c):
    print("\nThis showcases the Homomorphic property of Multiplication of a ciphertext by a plaintext")
    print("When a ciphertext is raised to the power of a plaintext, the result decrypts to the product of the two plaintexts")

    m3 = int(input("Pls input plaintext value of cipher that u want to be multiplied: "))
    c3p = c ** m3 % n**2
    
    print("C product is " + str(c3p))
    return c3p

# Annoymous secure voting..
def voting(n,g,lamda):
    Vsum = g**0 * 10**n % n**2
    
    print("\nThis showcases one of the practical uses of the Paillier Cryptosystem. Annoymous voting")
    for i in range(10):
        v = int(input("Pls input the value of your vote. 1 (yes), 0 (no)"))
        Rv = 9
        Vt = g**v * Rv**n % n**2
        Vsum *= Vt
    decryption(Vsum,n,lamda,g)
    print("This shows the number of people that voted yes.")
    

main_menu()
main()
