string_with_vows=input("Enter a sentence:")
sepd_lets=string_with_vows.split()
count=0
for i in range(len(string_with_vows)):
    if sepd_lets[i]=='a' or sepd_lets[i]=='e' or sepd_lets[i]=='i' or sepd_lets[i]=='o' or sepd_lets[i]=='u':
        count+=1
    else:
        pass
print(count)
print(sepd_lets)