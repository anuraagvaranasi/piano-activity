from run_server import match
from notes import Notes

#test if match can detect correct and incorrect sequences 
def test_match():
    #first test empty strings
    seq = ""
    assert match(seq) == False
    seq = "    "
    assert match(seq) == False
    #test some correct notes
    seq = "A B C D E"
    assert match(seq) == True
    seq = "A# Ab B# Bb C# Cb D# Db E# Eb F# Fb G# Gb"
    assert match(seq) == True
    seq = "A       B   C D     E"
    assert match(seq) == True
    #test some incorrect letters
    seq = "A B C D E F G H"
    assert match(seq) == False
    seq = "B3"
    assert match(seq) == False
    seq = "Ap Ab A# A$"
    assert match(seq) == False


#run all test functions in here
def main():
    test_match()

    
    print("Testing complete! No errors found!")


#run main function
if __name__ == "__main__":
    main()