from ag.connect_ag import Allegrograph
from classifier.kw_extract import extract_verb


def main():
  dranpto = Allegrograph(repo='dranpto', host="127.0.0.1", port=10035, user="test", pass_word="xyzzy", create=True, clear=False)
  user_input = input("Enter your search here: ")
  result = dranpto.get_statement(user_input)
  try:

    print("\nActual Result: ", result["Actual Result"])
    print("Free-text? : ", result["Free-text"])
    print("Question & Answer: ")
    for i in result["Suggested Questions"]:
      print("\n", i)
  except:
    print("\nActual Result: ", result)
    print("Result ends Here ---")




def run():
    main()

if __name__ == "__main__":
    run()

    
