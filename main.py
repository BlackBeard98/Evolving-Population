from Population import Population

print("Number of men (Enter for 100)")
men=input()
men=int(men) if men!="" else 100
print("Number of women (Enter for 100)")
women=input()
women=int(women) if women!="" else 100
print("Number of years (Enter for 100)")
years=input()
years=int(years) if years!="" else 100
p= Population(men,women,years)
p.run()
p.showdata()