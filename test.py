from tkinter import S


s1 = "<p>Hello my name is \n alvina Han<p/>"
s = "<p>Hello<p/><p><p/>"

# new = string.replace("<p>", "").replace("<p/>", "")

# print(new.split(" "))

end = s.find("<p/>") 
start = s.find("<p>")+3

print(s[start:end])