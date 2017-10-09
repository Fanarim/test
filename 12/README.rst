Number Echoer
===============

Usage
-------------
To run the program, follow the steps below:
::
  # go to the program's directory
  cd number_echoer/

  # Generate message catalogs:
  for LANGUAGE in `ls locale/ | grep -v .pot`; do msgfmt locale/$LANGUAGE/LC_MESSAGES/number_echoer.po -o locale/$LANGUAGE/LC_MESSAGES/number_echoer.mo; done;

  # Run the program in selected language:
  LANG=cs_CZ.UTF-8 ./number_echoer.py 12345
  LANG=de_DE.UTF-8 ./number_echoer.py 12345
  LANG=en_US.UTF-8 ./number_echoer.py 12345


Extracting messages
-------------------
To extract messages, run:
::
  xgettext number_echoer.py --add-comments -o locale/number_echoer.pot
