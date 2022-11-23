#include <stdio.h>
#include <stdlib.h>
#include <fstream>

#include <iostream>
#include <vector>
#include <climits>
#include <cmath>

#include "libscapi/include/comm/Comm.hpp"
#include "libscapi/include/infra/ConfigFile.hpp"

#include "include/HamParties.hpp"
#include "include/matrixDist.hpp"

#include "include/guide_tree.hpp"



float jukes_cantor(float diss)
{
    
    float jk = (diss != (float) 0) ? -3./4 * log( 1 - (4./3) * (1./diss) ) : 0;
    
    return jk;
}


int main(int argc, char* argv[])
{

    /**
     *                              INITIALIZATION
     * 
     * Initialize hamming party to compute hamming distances between every sequence 
     * 
     **/
    int numOfParties = atoi(argv[1]); // read from first argument input
    int partyNum = atoi(argv[2]); // read from second argument input
    int numOfInputs = atoi(argv[3]); // read from third argument input

    shared_ptr<HamParty> meHamParty = make_shared<HamParty>(partyNum, numOfParties, numOfInputs);

    cout << "PART 1 - COMPUTE HAMMING DISTANCES BETWEEN SEQUENCES" << endl;
    cout << "PART 1.1 - SEND NUMBER OF INPUTS \n" << endl;
    // Send number of inputs to other parties
    meHamParty->runNumberOfInputs();

    cout << "PART 1.2 - RUN HAMMING SMC \n" << endl;
    // Run Hamming SMC between every party present
    meHamParty->runHamSMC();

    cout << "PART 1.3 - SEND RESULTS \n" << endl;
    // Evaluators send (Garblers reveice) the results from Hamming SMC functionality
    meHamParty->evaluatorSendResultToGarbler();

    cout << "PART 1.4 - COMPUTE INTERNAL HAMMING DISTANCE \n" << endl;
    // Compute internal Hamming distances
    meHamParty->computeInternalHammingDistance();

    cout << "PART 1.5 - SEND/RECEIVE OTHER DISTANCES \n" << endl;
    // Send / Receive the other values
    meHamParty->sendAndReceiveOtherDistances();


    cout << "PART 2 - CREATE HAMMING DISTANCE MATRIX \n" << endl;
    shared_ptr<matrixDist> myMatrixDist = make_shared<matrixDist>(meHamParty);

    int n = myMatrixDist->n;
    vector<vector<float>> matrixDistance = myMatrixDist->mD;
    vector<string> mNodeNames = myMatrixDist->nodeNames;


    cout << "PART 2 - CREATE HAMMING DISTANCE MATRIX \n" << endl;
    fstream mDPhylipFile;


    cout << "PART 3 - SAVE MATRIX PHYLIP FORMAT \n" << endl;
    mDPhylipFile.open("../phylip-3.697/exe/infile",fstream::out);

    mDPhylipFile << n << "\n";

    for (int i=0; i<n;i++) //This variable is for each row below the x 
    {        
        mDPhylipFile << mNodeNames[i]<< "         ";

        for (int j=0; j<n;j++)
        {                      
            mDPhylipFile << jukes_cantor((float) matrixDistance[i][j]) << " ";
        }
        mDPhylipFile<<std::endl;
    }
    mDPhylipFile.close();
    
    
    //cout << "PART 3 - COMPUTE SECOND PART OF UPGMA \n" << endl;
    //GuideTree upgma_tree(n, matrixDistance, mNodeNames);
    //upgma_tree.CreateTree("upgma");

    //ofstream output_upgma("phylogeneticTree/upgma_tree.nwk");
    //upgma_tree.Output(output_upgma);
    //output_upgma.close();

    cout << "Clean up auxiliary informatin" << endl;

    // Remove files from results folder, otherwise the next run will get stuck (unkown issue solved)
    std::string del_script = "rm results/*";
    std::system(del_script.c_str()); 

    //cout << "DONE : Result saved to phylogeneticTree folder. \n";

    return 0;

}



