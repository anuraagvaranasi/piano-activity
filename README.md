# Piano Activity

## Additional Dependencies Required:
* SQLAlchemy
* SQLite3

## Features:
* Serves a sequence of notes by default rather than only one
* Server checks note pressed and provides feedback on whether it is correct or not
* Notes are changed to next note in sequence if correct note is played
* Data on correct/incorrect notes is stored, and returned back to user at completion 
* User data (username/password) is stored in a database (SQLite)
* Added login/register pages 
* Supports multiple users logging in and accessing the app
* Stores state of user sequence even through logouts
* Has an option for user to add their own sequence of notes to play
* Contains a file for testing components of app(test.py)

## Additional Features to add
* Sound on each keypress
* Storing object data in database too, so that user state is stored even through server restarts (currently loses progress when flask app is restarted)
* User can access a separate page to get a more detailed breakthrough of results 
* Users can access previous results and see changes 
* Add many many more tests to test.py (currently only tests the match function)
