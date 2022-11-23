#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <boost/filesystem.hpp>
#include <iostream>
#include <nlohmann/json.hpp>
#include "etsi_qkd_004.hpp"
#include <stdexcept>
#include <thread>
#include <bitset>
//#include <vector>

#include "qlibscapi/include/comm/Comm.hpp"
#include "qlibscapi/include/infra/ConfigFile.hpp"

string preprocessInput(string path);
float dissimilarity(string input_i, string input_j);
int hammingDistance(string input_i, string input_j);
unsigned int encrypt32bits(vector<unsigned char>& cumulative_qkd_buffer, unsigned int msg);
string encryptString(vector<unsigned char>& cumulative_qkd_buffer, string yaoResult);
string decryptString(vector<unsigned char>& cumulative_qkd_buffer, string yaoResult);

class HamParty
{
private:

public:
    HamParty(int id, int numOfParties, int numOfInputs);

    int id;
    int numOfParties;
    int numOfInputs;

    vector<int> numOfInputsOtherParties;

    vector<string> qkd_uris;
    vector<string> qokd_uris;

    vector<string> qkd_ksid;
    vector<string> qokd_ksid;

    vector<etsi_qkd_004::KeyBuffer> cumulative_qkd_buffer;
    vector<etsi_qkd_004::KeyBuffer> cumulative_qokd_buffer;

    string lkms_ip;
    string lkms_port;

    //ConfigFile configFile;
    
    vector<int> ports;
    vector<string> ips;

    vector<vector<int>> results;

    void runNumberOfInputs();

    void getAddressLKMS();

    void getAddressQKD();

    void getAddressQOKD();

    void getKsidQKD();

    void getKsidQOKD();

    void generateQKDKeys();

    void generateQOKDKeys();

    void runHamSMC();

    void evaluatorSendResultToGarbler();

    void computeInternalHammingDistance();

    void sendAndReceiveOtherDistances();

    //vector<vector<int>> mat(int numOfcols, vector<int>(numOfrows)); // Definir a matrix!



};
