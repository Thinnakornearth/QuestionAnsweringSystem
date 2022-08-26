from ag.connect_ag import Allegrograph
from classifier.kw_extract import extract_verb


def main():
  dranpto = Allegrograph(repo='dranpto', host="127.0.0.1", port=10035, user="test", pass_word="xyzzy", create=True, clear=False)
  user_input = input("Enter your search here: ")
  result = dranpto.get_statement(user_input)
  try:
    for i in result:
      print("\nActual Result: ", i)
  except:
    None




def run():
    main()

if __name__ == "__main__":
    run()