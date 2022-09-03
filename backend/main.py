from ag.connect_ag import Allegrograph
from classifier.kw_extract import extract_verb


def main():
  dranpto = Allegrograph(repo='dranpto', host="10.14.109.78", port=10035, user="thinnakorn", pass_word="Earth6210", create=True, clear=False)
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




def run():
    main()

if __name__ == "__main__":
    run()

    
