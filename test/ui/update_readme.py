filelength = len(open("test.log",'r').readlines())
test_report = open("test.log",'r').readlines()[filelength-5:]
filelength = len(open("readme.md",'r').readlines())
readme_text = open("readme.md",'r').readlines()[:filelength-5]
with open("readme.md",'w') as rm:
    with open("test.log",'r') as log:
        readme_text = "".join(readme_text)
        rm.write(readme_text)
        test_report = "".join(test_report)
        rm.write(test_report)
print("Done!")