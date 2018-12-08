## Blockchain vs Tangle

Hey Ruslan, 

I made you a readme just in case you need anything clarified. 

I made you a requirements.txt file that should cover all the dependencies. It can all be downloaded with pip

I separated the blockchain and the tangle into 2 separate directories. 

Once you get into either directory, set up 2 screen: 

 - on screen #1, "python blockchain.py <size_of_sample>" is all you need to do, with <size_of_sample> being any option you choose from the 5 options in the paper [5, 50, 500, 5000, 50000, 500000]. Same thing for tangle, just run "python tangle.py <size_of_sample>"
 - on screen #2, "python run.py" is all you need. This triggers a request to the server to load the transactions and open up mining through the loop. 

 I takes a while to run, so if you don't want to wait around, check out the output of tqdm. It will give you 3 pieces of information:
 a) the iterations per second rate (which we used for our sub 0s estimates)
 b) a progress bar showing how far into the process the program is
 c) a remarkably accurate estimate of how long the process will take. 

I also included the script we used to generate our testing set with transactions. "python generateTransactions.py" is all you need for that. Feel free to play with it if you'd like XD

Lorenzo 