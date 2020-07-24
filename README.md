# AgendaManager
This is the code for the project of Natural Language Interaction, part of the Master in Intelligent Interactive Systems at UPF (year 2019/2020). We were short in time and the system can be improved a lot. 

The code consists of:

* **agenda_manager_system**

    - *agenda_manager.py*: Implements the Logic of the system.
    - *dialogue_manager.py*: Implements the dialogue manager.
    - *generation.py*: Functions to generate sentences.
    - *asr_parser.py*: Contains the function to call the ASR and the ones needed for parsing and PoS
    - *TTS.py*: Module that includes the Text-to-Speech system.
    
* **main.py** Just the main executable, but rather use ```source execute.sh``` or ```./execute.sh``` due to changes on the ```PYTHONPATH.

The file agenda.csv keeps all the information of the agenda.
