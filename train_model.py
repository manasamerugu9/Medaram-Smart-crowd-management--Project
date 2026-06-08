people = int(input("Enter people count: "))

if people <= 500:
    print("Crowd Status: Low")
    print("Area is safe")

elif people <= 8000:
    print("Crowd Status: Medium")
    print("Crowd is increasing")

elif people <= 80000:
    print("Crowd Status: High")
    print("Warning: Heavy crowd detected")

else:
    print("Crowd Status: Dangerous")
    print("ALERT! Emergency support needed")
    people = int(input("Enter people count: "))

# GREEN
if people <= 500:
    print("\033[92m")
    print("Crowd Status: Low")
    print("Area is safe")

# YELLOW
elif people <= 8000:
    print("\033[93m")
    print("Crowd Status: Medium")
    print("Crowd is increasing")

# RED
elif people <= 80000:
    print("\033[91m")
    print("Crowd Status: High")
    print("Warning: Heavy crowd detected")

# DARK RED
else:
    print("\033[31m")
    print("Crowd Status: Dangerous")
    print("ALERT! Emergency support needed")

# RESET COLOR
print("\033[0m")
