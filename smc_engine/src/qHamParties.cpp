#include "../include/qHamParties.hpp"


HamParty::HamParty(int id, int numOfParties, int numOfInputs)
{
    this-> id = id;
    this-> numOfParties = numOfParties;
    this-> numOfInputs = numOfInputs;
    
    // Initialization numOfOtherParties
    vector<int> numOfInputsOtherParties(numOfParties, 0);
    numOfInputsOtherParties[id] = numOfInputs;
    this->numOfInputsOtherParties = numOfInputsOtherParties;

    // Initialization of QKD URI vector
    vector<string> qkd_uris(numOfParties, "0");
    this->qkd_uris = qkd_uris;

    // Initialization of QOKD URI vector
    vector<string> qokd_uris(numOfParties, "0");
    this->qokd_uris = qokd_uris;

    // Initialization of QKD ksid
    vector<string> qkd_ksid(numOfParties, "0");
    this->qkd_ksid = qkd_ksid;

    // Initialization of QOKD ksid
    vector<string>  qokd_ksid(numOfParties, "0");
    this->qokd_ksid = qokd_ksid;

    // Initialization of QKD key buffer;
    etsi_qkd_004::KeyBuffer empty_qkd_buffer;
    vector<etsi_qkd_004::KeyBuffer> cumulative_qkd_buffer(numOfParties, empty_qkd_buffer);
    this->cumulative_qkd_buffer = cumulative_qkd_buffer;

    // Initialization of QOKD key buffer;
    etsi_qkd_004::KeyBuffer empty_qokd_buffer;
    vector<etsi_qkd_004::KeyBuffer> cumulative_qokd_buffer(numOfParties, empty_qokd_buffer);
    this->cumulative_qokd_buffer = cumulative_qokd_buffer;
    
    // Extract ips and port vlaues
    ConfigFile cf("partiesFiles/Parties");

    string portString, ipString;
    vector<int> ports(numOfParties);
    vector<string> ips(numOfParties);
    //int counter = 0;
    for(int i=0; i < numOfParties; i++)
    {
        portString = "party_" + to_string(i) + "_port";
        ipString = "party_" + to_string(i) + "_ip";
        // Get parties IPs and ports data
        ports[i] = stoi(cf.Value("", portString));
        ips[i] = cf.Value("", ipString);
    }

    this->ports = ports;
    this->ips = ips;

    // Create YaoConfig files for each input
    for(int i=0; i < numOfInputs; i++)
    {
        ofstream yaoConfigFile;
        std::string yaoConfigFileName = "yaoConfigFiles/YaoConfig_seq_";
        yaoConfigFileName += to_string(i); 
        yaoConfigFileName += ".txt";

        yaoConfigFile.open(yaoConfigFileName);

        yaoConfigFile << "print_output = true\n";
        yaoConfigFile << "input_section = AES\n";
        yaoConfigFile << "circuit_type = NoFixedKey\n";
        yaoConfigFile << "\n";
        yaoConfigFile << "# OS name is added automatically\n";
        yaoConfigFile << "[AES-Linux]\n";
        yaoConfigFile << "circuit_file = boolCircuit/mainScapi.txt\n";
        yaoConfigFile << "input_file_party_1 = inputFiles/Party_" + to_string(id) + "_seq_" + to_string(i) + ".txt\n";
        yaoConfigFile << "input_file_party_2 = inputFiles/Party_" + to_string(id) + "_seq_" + to_string(i) + ".txt\n";

        yaoConfigFile.close();
    }

}


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                              PART 1.1 - SEND NUMBER OF INPUTS


void HamParty::runNumberOfInputs()
{
    int partyNum = this->id;
    int numOfParties = this->numOfParties;
    int numOfInputs = this->numOfInputs;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;

    SocketPartyData me, other;
    boost::asio::io_service io_service;

    // for each party
    for(int i=0; i < numOfParties; i++)
    {
        if(i < partyNum) 
        {// Evaluator - Send result

            int myPort = ports[partyNum] + i*10;
            int otherPort = ports[i] + partyNum*10 - 10;

            
            cout <<"SEND NUMBER OF INPUTS TO PARTY " + to_string(i) <<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<< myPort <<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<< otherPort <<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;
            
            cout <<"RECEIVE NUMBER OF INPUTS FROM PARTY " + to_string(i) <<endl;
            // send number of inputs
            channel->writeWithSize(to_string(numOfInputs)); // TODO: Encrypt the communication

            // Receive number of inputs from i
            string numberOfInputsOtherParty;
            vector<byte> raw_numberOfInputsOtherParty;
            channel->readWithSizeIntoVector(raw_numberOfInputsOtherParty); // TODO: Encrypt the communication
            const byte * uc = &(raw_numberOfInputsOtherParty[0]);
            numberOfInputsOtherParty = string(reinterpret_cast<char const *>(uc), raw_numberOfInputsOtherParty.size());

            this-> numOfInputsOtherParties[i] = stoi(numberOfInputsOtherParty);
            


        }else if(i > partyNum)
        {// Garbler - Receive result
            
            int myPort = ports[partyNum] + i*10 - 10;
            int otherPort = ports[i] + partyNum*10;

            
            cout <<"RECEIVE NUMBER OF INPUTS FROM PARTY " + to_string(i) <<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<<myPort<<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<<otherPort<<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;

            // Receive
            string numberOfInputsOtherParty;
            vector<byte> raw_numberOfInputsOtherParty;
            channel->readWithSizeIntoVector(raw_numberOfInputsOtherParty); // TODO: Encrypt the communication
            const byte * uc = &(raw_numberOfInputsOtherParty[0]);
            numberOfInputsOtherParty = string(reinterpret_cast<char const *>(uc), raw_numberOfInputsOtherParty.size());

            this-> numOfInputsOtherParties[i] = stoi(numberOfInputsOtherParty);

            cout <<"SEND NUMBER OF INPUTS TO PARTY " + to_string(i) <<endl;
            // send number of inputs
            channel->writeWithSize(to_string(numOfInputs)); // TODO: Encrypt the communication

            


        }
    }

}


//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //





// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                      PART 1.2 - GENERATE QKD AND QOKD KEYS


//  _________________________________________________________________________________________________________________________ //
//
//                                               Send/Build URI vector
//  _________________________________________________________________________________________________________________________ //


void HamParty::getAddressLKMS()
{ // TODO: this is hardcoded

    this->lkms_ip = "127.0.0.1";
    this->lkms_port = "44441";
}


void HamParty::getAddressQKD()
{
    //int partyNum = this->id;
    //int numOfParties = this->numOfParties;
    //int numOfInputs = this->numOfInputs;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;
                                                      
    vector<string> hardcoded_qkd_uri = {"qkd:Application1@aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "qkd:Application1@bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "qkd:Application1@cccccccc-cccc-cccc-cccc-cccccccccccc"};

    for(int i=0; i < numOfParties; i++)
    {
        this->qkd_uris[i] = hardcoded_qkd_uri[i];
    }

}


void HamParty::getAddressQOKD()
{
    //int partyNum = this->id;
    //int numOfParties = this->numOfParties;
    //int numOfInputs = this->numOfInputs;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;
                                                      
    vector<string> hardcoded_qokd_uri = {"qokd:Application1@aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "qokd:Application1@bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "qokd:Application1@cccccccc-cccc-cccc-cccc-cccccccccccc"};

    for(int i=0; i < numOfParties; i++)
    {
        this->qokd_uris[i] = hardcoded_qokd_uri[i];
    }

}

void HamParty::getKsidQKD()
{
    int partyNum = this->id;
    int numOfParties = this->numOfParties;

    string hardcoded_qkd_ksid[3][3] = {
        {"", "14354992-1234-1234-1234-123456789001", "14354992-1234-1234-1234-123456789002"},
        {"14354992-1234-1234-1234-123456789001", "", "14354992-1234-1234-1234-123456789012"},
        {"14354992-1234-1234-1234-123456789002", "14354992-1234-1234-1234-123456789012", "" }
        };

    for(int i=0; i < numOfParties; i++)
    {
        this->qkd_ksid[i] = hardcoded_qkd_ksid[i][partyNum];
    }
    
}

void HamParty::getKsidQOKD()
{
    int partyNum = this->id;
    int numOfParties = this->numOfParties;

    string hardcoded_qokd_ksid[3][3] = {
        {"", "14354992-1234-1234-1234-123456789101", "14354992-1234-1234-1234-123456789102"},
        {"14354992-1234-1234-1234-123456789101", "", "14354992-1234-1234-1234-123456789112"},
        {"14354992-1234-1234-1234-123456789102", "14354992-1234-1234-1234-123456789112", "" }
        };

    for(int i=0; i < numOfParties; i++)
    {
        this->qokd_ksid[i] = hardcoded_qokd_ksid[i][partyNum];
    }    
}




//  _________________________________________________________________________________________________________________________ //
//
//                                                       QKD generation
//  _________________________________________________________________________________________________________________________ //

void HamParty::generateQKDKeys()
{

    int partyNum = this->id;
    int numOfParties = this->numOfParties;
    //int numOfInputs = this->numOfInputs;
    vector<int> numOfInputsOtherParties = this->numOfInputsOtherParties;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;
    vector<string> qkd_uris = this->qkd_uris;

    string source = this->qkd_uris[partyNum];

    // Address of this party's LKMS
    etsi_qkd_004::LKMSAddress address = {this->lkms_ip, (unsigned short) stoi(this->lkms_port)}; 
    std::cout << "Using address: " << address.ip << ':' << address.port << std::endl;

    // Configure desired key (CHUNK_SIZE * CHUNK_NUMBER in bytes)
    const unsigned int CHUNK_SIZE = 4;  // Number of key bytes retrieved per GET_KEY (we want it to be 32 bites)
    vector<unsigned int> CHUNK_NUMBER(numOfParties, 2);  // Number of key chunks you want to get
    for(int i=0; i < numOfParties; i++)
    {
        if(i != partyNum)
        {// Evaluator
            // Keys: after yao gc evaluation
            int chk_nr_yao = numOfInputsOtherParties[i] * numOfInputsOtherParties[partyNum]; 

            // Keys: distance distribution phase
            int chk_nr_internal_computation_send = numOfInputsOtherParties[partyNum] * (numOfInputsOtherParties[partyNum] - 1)/2;
            int chk_nr_internal_computation_rec = numOfInputsOtherParties[i] * (numOfInputsOtherParties[i] - 1)/2;
            int chk_nr_other_yao_send = 0;
            for(int j=0; j < numOfParties; j++)
            {
                if(j != i && j!=partyNum)
                {
                    chk_nr_other_yao_send = chk_nr_other_yao_send + numOfInputsOtherParties[j] * numOfInputsOtherParties[partyNum];
                } 
            }

            int chk_nr_other_yao_rec = 0;
            for(int j=0; j < numOfParties; j++)
            {
                if(j != i && j!=partyNum)
                {
                    chk_nr_other_yao_rec = chk_nr_other_yao_rec + numOfInputsOtherParties[j] * numOfInputsOtherParties[i];
                } 
            }

            // total chunck number
            unsigned int total_chk_nr = chk_nr_yao + chk_nr_internal_computation_send + chk_nr_internal_computation_rec + chk_nr_other_yao_send + chk_nr_other_yao_rec;

            CHUNK_NUMBER[i] = total_chk_nr;
        }
    }

    // for each party
    for(int i=0; i < numOfParties; i++)
    {
        if(i != partyNum) 
        {
            // ----- OPEN_CONNECT -----
            std::string destination = this->qkd_uris[i];  // Classic key

            etsi_qkd_004::QoS qos = {CHUNK_SIZE, 32, 32, 0, 0, 150000, 0, ""};
            string ksid = this->qkd_ksid[i];
            auto oc_response = etsi_qkd_004::open_connect(address, source, destination, qos, ksid);
            std::cout << "OPEN CONNECT STATUS: " << oc_response.status << std::endl;

            // ----- GET_KEY -----
            unsigned int index = 0;
            while (index < CHUNK_NUMBER[i]) {
                //std::this_thread::sleep_for(std::chrono::milliseconds(1000));
                auto gk_response = etsi_qkd_004::get_key(address, oc_response.key_stream_id, index);
                
                while(gk_response.status != etsi_qkd_004::Status::SUCCESSFUL)
                {
                    gk_response = etsi_qkd_004::get_key(address, oc_response.key_stream_id, index);
                    std::cout << "ERROR: Status " << gk_response.status << std::endl;
                    std::cout << "Waiting for successful status" << std::endl;
                    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
                }
                
                if (gk_response.status == etsi_qkd_004::Status::SUCCESSFUL) {
                     std::cout << "Generating key nr " << index << std::endl;
                    // Extend cumulative_key_buffer
                    this->cumulative_qkd_buffer[i].reserve(this->cumulative_qkd_buffer[i].size() +
                                                std::distance(gk_response.key_buffer.cbegin(),
                                                                gk_response.key_buffer.cend()));
                    this->cumulative_qkd_buffer[i].insert(this->cumulative_qkd_buffer[i].cend(), gk_response.key_buffer.cbegin(),
                                                gk_response.key_buffer.cend());
                    // Increment chunk index (only if gk_response.status is SUCCESSFUL)
                    ++index;
                }else
                {
                    std::cout << "FINAL ERROR: Status " << gk_response.status << ". Did not generated correctly the quantum keys." << std::endl;
                }     
            }

            // ----- CLOSE -----
            auto cl_response = etsi_qkd_004::close(address, oc_response.key_stream_id);
            std::cout << "CLOSE STATUS: " << cl_response.status << std::endl;
        }
    }

}

//  _________________________________________________________________________________________________________________________ //
//
//                                                        QOKD generation
//  _________________________________________________________________________________________________________________________ //

/**
 * 
 * 
 *                      This generates a .txt file with the following structure:
 *                          SizeKeys: 512
 *                          NumberKeys: 50
 *                          001010110011010010010101010010010100\n
 *                          111001001011010010010101010100100101\n
 * 
 * 
 * 
 * 
 * 
 * */


void HamParty::generateQOKDKeys()
{

    int partyNum = this->id;
    int numOfParties = this->numOfParties;
    //int numOfInputs = this->numOfInputs;
    vector<int> numOfInputsOtherParties = this->numOfInputsOtherParties;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;
    vector<string> qokd_uris = this->qokd_uris;

    string source = this->qokd_uris[partyNum];

    // Address of this party's LKMS
    etsi_qkd_004::LKMSAddress address = {this->lkms_ip, (unsigned short) stoi(this->lkms_port)}; 
    std::cout << "Using address: " << address.ip << ':' << address.port << std::endl;

    // Configure desired key (CHUNK_SIZE * CHUNK_NUMBER in bytes)
    const unsigned int CHUNK_SIZE = 64;  // Number of key bytes retrieved per GET_KEY (we want it to be 32 bites)
    vector<unsigned int> CHUNK_NUMBER(numOfParties, 2);  // Number of key chunks you want to get

    for(int i=0; i < numOfParties; i++)
    {
        if(i != partyNum)
        {// Evaluator
            // Keys: after yao gc evaluation
            int chk_nr_yao = numOfInputsOtherParties[i] * numOfInputsOtherParties[partyNum] * 128; 

            CHUNK_NUMBER[i] = chk_nr_yao;
        }
    }



    // for each party
    for(int i=0; i < numOfParties; i++)
    {
        if(i != partyNum) 
        {
            // ----- CREATE FILE ------
            string role = (i < partyNum) ? "alice" : "bob"; // Recall that Alice and Bob have revert roles
            string file_path = "quantum_oblivious_key_distribution/signals/ok_" + role + "_" + to_string(i) + ".txt";
            std::ofstream file(file_path);

            // Write header:
            file << "Role: " + role << endl;
            file << "IPOtherParty: " + ips[i] << endl;
            file << "SizeOKeys: 512" << endl;
            file << "NumberOKeys: " + to_string(CHUNK_NUMBER[i]) << endl;

            // ----- OPEN_CONNECT -----
            std::string destination = this->qokd_uris[i];  // Classic key

            etsi_qkd_004::QoS qos = {CHUNK_SIZE, 1024, 1024, 0, 0, 150000, 0, ""};
            //string ksid = this->qokd_ksid[i];
            string ksid = this->qokd_ksid[i];
            auto oc_response = etsi_qkd_004::open_connect(address, source, destination, qos, ksid, role);
            std::cout << "OPEN CONNECT STATUS: " << oc_response.status << std::endl;

            // ----- GET_KEY -----
            unsigned int index = 0;
            while (index < CHUNK_NUMBER[i]) {
                //std::this_thread::sleep_for(std::chrono::milliseconds(1000));
                auto gk_response = etsi_qkd_004::get_key(address, oc_response.key_stream_id, index);
                
                while(gk_response.status != etsi_qkd_004::Status::SUCCESSFUL)
                {
                    gk_response = etsi_qkd_004::get_key(address, oc_response.key_stream_id, index);
                    std::cout << "ERROR: Status " << gk_response.status << std::endl;
                    std::cout << "Waiting for successful status" << std::endl;
                    std::this_thread::sleep_for(std::chrono::milliseconds(100));
                }
                
                if (gk_response.status == etsi_qkd_004::Status::SUCCESSFUL) {
                    std::cout << "Generating oblivious key nr " << index << std::endl;

                    // Build key part of oblivious key file
                    for(char key : gk_response.key_buffer)
                    {
                        string readable_key = bitset<8>(key).to_string();
                        file << readable_key;
                    } 
                    file << endl;

                    // Increment chunk index (only if gk_response.status is SUCCESSFUL)
                    ++index;
                }else
                {
                    std::cout << "FINAL ERROR: Status " << gk_response.status << ". Did not generated correctly the quantum keys." << std::endl;
                }     
            }

            // ----- CLOSE -----
            auto cl_response = etsi_qkd_004::close(address, oc_response.key_stream_id);
            std::cout << "CLOSE STATUS: " << cl_response.status << std::endl;
        }
    }


}



//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //






// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                      PART 1.3 - RUN HAMMING SMC BETWEEN TWO PARTIES


void HamParty::runHamSMC()
{

    int partyNum = this->id;
    int numOfParties = this->numOfParties;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;

    // for each party
    for(int i=0; i < numOfParties; i++)
    {
        int numOfInputsOtherParty = this->numOfInputsOtherParties[i];

        if(i < partyNum)
        {// Evaluator

            cout << "EVALUATOR STARTING" << endl;

            int myPort = ports[partyNum] + i*10 - 10;
            int otherPort = ports[i] + partyNum*10;

            // Create Parties file ===========================
            ofstream PartiesFile;
            string partiesFile_name = "partiesFiles/Parties_" + to_string(partyNum) + "_" + to_string(i);
            PartiesFile.open(partiesFile_name);

            PartiesFile << "party_0_ip = " + ips[i] + "\n";
            PartiesFile << "party_1_ip = " + ips[partyNum]  + "\n";
            PartiesFile << "party_0_port = " + to_string(otherPort) + "\n";
            PartiesFile << "party_1_port = " + to_string(myPort) + "\n";

            PartiesFile.close();
            // ==============================================

            // Rename oblivious key file ====================
            string role = (i < partyNum) ? "alice" : "bob"; // Recall that Alice and Bob have revert roles
            string old_file_path = "quantum_oblivious_key_distribution/signals/ok_" + role + "_" + to_string(i) + ".txt";
            string new_file_path = "quantum_oblivious_key_distribution/signals/oblivious_keys.txt";
            string run_script_before_yao = "mv ";
            run_script_before_yao += old_file_path;
            run_script_before_yao += " ";
            run_script_before_yao += new_file_path;

            std::system(run_script_before_yao.c_str()); 
            // ==============================================

            // SMC for all inputs 
            for(int j=0; j < numOfInputs; j++)
            {// for each myInput

                for(int k=0; k < numOfInputsOtherParty; k++)
                {

                    cout << "Computing hamming distance between myseq " + to_string(j) + " and otherseq " + to_string(k) << endl;
                    // Run SMC between evaluator and garbler=======
                    std::string run_script = "./qrunSMCParty.sh ";
                    run_script += to_string(1);
                    run_script += " yaoConfigFiles/YaoConfig_seq_" + to_string(j) + ".txt ";
                    run_script += partiesFile_name;

                    std::cout << "Running Yao protocol between my port "<< myPort << " and other port "<< otherPort <<endl;
                    // run ./sunSMCParty.sh
                    std::system(run_script.c_str()); 
                    std::cout <<"Finnished Yao protocol"<<endl;

                    std::cout <<"Waiting for 1 second"<<endl;
                    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

                    // kill process 
                    std::string kill_process = "kill $(lsof -t -i:" + to_string(myPort) + ")";
                    std::system(kill_process.c_str());
                    std::string kill_process_obliv = "kill $(lsof -t -i:" + to_string(myPort+1) + ")";
                    std::system(kill_process_obliv.c_str());
                    std::cout <<"Yao protocol process killed on port "<< myPort <<endl;
                    std::cout <<"\n"<<endl;
                    // ============================================

                    // Rename output file =====
                    std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                    newYaoOutputFileName += "otherparty_";
                    newYaoOutputFileName += to_string(i); 
                    newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                    rename("output_file.txt", newYaoOutputFileName.c_str());
                    // ========================
                }

            }

            // Rename oblivious key file ====================
            string run_script_after_yao = "mv ";
            run_script_after_yao += new_file_path;
            run_script_after_yao += " ";
            run_script_after_yao += old_file_path;

            std::system(run_script_after_yao.c_str()); 
            // ==============================================



        }else if(i > partyNum)
        {// Garbler 

            cout << "GARBLER STARTING" << endl;

            int myPort = ports[partyNum] + i*10;
            int otherPort = ports[i] + partyNum*10 - 10;
            // Create Parties file ==========================
            ofstream PartiesFile;
		    
            string partiesFile_name = "partiesFiles/Parties_" + to_string(partyNum)  + "_" + to_string(i) ;
            PartiesFile.open(partiesFile_name);

            PartiesFile << "party_0_ip = " + ips[partyNum] + "\n";
            PartiesFile << "party_1_ip = " + ips[i] + "\n";
            PartiesFile << "party_0_port = " + to_string(myPort) + "\n";
            PartiesFile << "party_1_port = " + to_string(otherPort) + "\n";

            PartiesFile.close();
            // ==============================================


            // Rename oblivious key file ====================
            string role = (i < partyNum) ? "alice" : "bob"; // Recall that Alice and Bob have revert roles
            string old_file_path = "quantum_oblivious_key_distribution/signals/ok_" + role + "_" + to_string(i) + ".txt";
            string new_file_path = "quantum_oblivious_key_distribution/signals/oblivious_keys.txt";
            string run_script_before_yao = "mv ";
            run_script_before_yao += old_file_path;
            run_script_before_yao += " ";
            run_script_before_yao += new_file_path;

            std::system(run_script_before_yao.c_str()); 
            // ==============================================

            // SMC for all inputs 
            for(int k=0; k < numOfInputsOtherParty; k++)
            {// for each myInput
                for(int j=0; j < numOfInputs; j++)
                {   
                    cout << "Computing hamming distance between myseq " + to_string(j) + " and otherseq " + to_string(k) << endl;
                    // Run SMC between evaluator and garbler=======
                    std::string run_script = "./qrunSMCParty.sh ";
                    run_script += to_string(0);
                    run_script += " yaoConfigFiles/YaoConfig_seq_" + to_string(j) + ".txt ";
                    run_script += partiesFile_name;
                    cout << "Running Yao protocol between my port "<< myPort << " and other port "<< otherPort <<endl;
                    // run ./sunSMCParty.sh
                    system(run_script.c_str());
                    cout <<"Finnished Yao protocol"<<endl;

                    std::cout <<"Waiting for 1 second"<<endl;
                    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

                    // kill process 
                    std::string kill_process = "kill $(lsof -t -i:" + to_string(myPort) + ")";
                    std::system(kill_process.c_str());
                    std::string kill_process_obliv = "kill $(lsof -t -i:" + to_string(myPort+1) + ")";
                    std::system(kill_process_obliv.c_str());
                    std::cout <<"Yao protocol process killed on port "<< myPort <<endl;
                    cout <<"\n"<<endl;
                    // ============================================
                }
            }

            // Rename oblivious key file ====================
            string run_script_after_yao = "mv ";
            run_script_after_yao += new_file_path;
            run_script_after_yao += " ";
            run_script_after_yao += old_file_path;

            std::system(run_script_after_yao.c_str()); 
            // ==============================================

        }



    }

};

//                                     

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                      PART 1.4 - EVALUATOR SEND RESULTS TO GARBLER


void HamParty::evaluatorSendResultToGarbler()
{
    int partyNum = this->id;
    int numOfParties = this->numOfParties;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;

    SocketPartyData me, other;
    boost::asio::io_service io_service;

    for(int i=0; i < numOfParties; i++)
    {
        int numOfInputsOtherParty = this->numOfInputsOtherParties[i];

        if(i < partyNum)
        {// Evaluator - Send result

            int myPort = ports[partyNum] + i*10;
            int otherPort = ports[i] + partyNum*10 - 10;

            
            cout <<"SEND RESULTS"<<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<< myPort <<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<< otherPort <<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;

            // SMC for all inputs 
            for(int j=0; j < numOfInputs; j++)
            {// for each myInput

                for(int k=0; k < numOfInputsOtherParty; k++)
                {

                    std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                    newYaoOutputFileName += "otherparty_";
                    newYaoOutputFileName += to_string(i); 
                    newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";

                    ifstream yaoOutput(newYaoOutputFileName);
                    std::string yaoResult;
                    std::getline(yaoOutput, yaoResult);

                    // Encrypt and send
                    std::string encrypted_yaoResult;
                    encrypted_yaoResult = encryptString(this->cumulative_qkd_buffer[i], yaoResult);
                    channel->writeWithSize(encrypted_yaoResult);
                }

            }
            


        }else if(i > partyNum)
        {// Garbler - Receive result
            
            int myPort = ports[partyNum] + i*10 - 10;
            int otherPort = ports[i] + partyNum*10;

            
            cout <<"RECEIVE RESULTS"<<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<<myPort<<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<<otherPort<<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;

            for(int k=0; k < numOfInputsOtherParty; k++)
            {// for each myInput
                for(int j=0; j < numOfInputs; j++)
                {  
                    // Initialize
                    string yaoResult;
                    string decrypt_yaoResult;
                    vector<byte> raw_yaoResult;

                    // Recieve from channel
                    channel->readWithSizeIntoVector(raw_yaoResult); // TODO: Encrypt the communication
                    
                    // From vector to string
                    const byte * uc = &(raw_yaoResult[0]);
                    yaoResult = string(reinterpret_cast<char const *>(uc), raw_yaoResult.size());

                    // Decrypt
                    decrypt_yaoResult = decryptString(this->cumulative_qkd_buffer[i], yaoResult);
                    
                    // Save to file
                    ofstream yaoOutputFile;

                    std::string YaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                    YaoOutputFileName += "otherparty_";
                    YaoOutputFileName += to_string(i); 
                    YaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                    
                    yaoOutputFile.open(YaoOutputFileName);
                    yaoOutputFile << decrypt_yaoResult;
                    yaoOutputFile.close();
            
                }
            }   
        }
    }
}

//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                      PART 1.5 - COMPUTE INTERNAL HAMMING DISTANCE


void HamParty::computeInternalHammingDistance()
{
    int numOfInputs = this->numOfInputs;
    int id = this->id;

    for(int i = 0; i < numOfInputs; i++)
    {
        for(int j = i + 1; j < numOfInputs; j++)
        {

            // Convert format
            string filename_i = "inputFiles/Party_" + to_string(id) + "_seq_" + to_string(i) + ".txt";
            string inputSeq_i;
            inputSeq_i = preprocessInput(filename_i);

            string filename_j = "inputFiles/Party_" + to_string(id) + "_seq_" + to_string(j) + ".txt";
            string inputSeq_j;
            inputSeq_j = preprocessInput(filename_j);

            // Compute Dissimilarity distance
            float diss;
            diss = dissimilarity(inputSeq_i, inputSeq_j);

            // save to file
            ofstream outputFile;

            std::string outputFileName = "results/out_myseq_" + to_string(i) + "_";
            outputFileName += "otherparty_";
            outputFileName += to_string(id); 
            outputFileName += "_otherseq_" + to_string(j) + ".txt";
            
            outputFile.open(outputFileName);
            outputFile << diss;
            outputFile.close();

        }
    }


}

//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                      PART 1.6 - SEND/RECEIVE OTHER DISTANCES


void HamParty::sendAndReceiveOtherDistances()
{

    int partyNum = this->id;
    int numOfParties = this->numOfParties;

    vector<int> ports = this->ports;
    vector<string> ips = this->ips;

    SocketPartyData me, other;
    boost::asio::io_service io_service;

    for(int i=0; i < numOfParties; i++)
    {
        int numOfInputsOtherParty = this->numOfInputsOtherParties[i];

        if(i < partyNum)
        {// Evaluator - Send result

            int myPort = ports[partyNum] + i*10;
            int otherPort = ports[i] + partyNum*10 - 10;

            
            cout <<"SEND RESULTS"<<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<< myPort <<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<< otherPort <<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;

            cout << "EVALUATOR INTERNAL SENDING..." << endl;
            // Send internal results
            for(int j = 0; j < numOfInputs; j++)
            {
                for(int k = j + 1; k < numOfInputs; k++)
                {   
                    cout << "I AM SENDING..." << endl;
                    std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                    newYaoOutputFileName += "otherparty_";
                    newYaoOutputFileName += to_string(partyNum); 
                    newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";

                    ifstream yaoOutput(newYaoOutputFileName);
                    std::string yaoResult;
                    std::getline(yaoOutput, yaoResult);

                    // Encrypt and send
                    // Note: type of internal computation is int. Thus, we need to compute encryption differently
                    std::string encrypted_yaoResult;
                    unsigned int encrypted_yaoResult_uint32;
                    unsigned int yaoResult_int = (unsigned int)std::stoi(yaoResult);

                    encrypted_yaoResult_uint32 = encrypt32bits(this->cumulative_qkd_buffer[i], yaoResult_int); // cipher function = decipher function
                    encrypted_yaoResult = bitset<32>(encrypted_yaoResult_uint32).to_string();

                    channel->writeWithSize(encrypted_yaoResult);
                }
            }

            cout << "EVALUATOR RECEIVING..." << endl;
            // Receive internal results
            for(int j = 0; j < numOfInputsOtherParty; j++)
            {
                for(int k = j + 1; k < numOfInputsOtherParty; k++)
                {
                    // Initialization
                    string yaoResult;
                    string decrypt_yaoResult;
                    vector<byte> raw_yaoResult;

                    // Receive from channel
                    channel->readWithSizeIntoVector(raw_yaoResult);

                    // From vector to string
                    const byte * uc = &(raw_yaoResult[0]);
                    yaoResult = string(reinterpret_cast<char const *>(uc), raw_yaoResult.size());

                    // Decrypt
                    decrypt_yaoResult = decryptString(this->cumulative_qkd_buffer[i], yaoResult);

                    // save to file
                    ofstream yaoOutputFile;

                    std::string YaoOutputFileName = "results/out_party_" + to_string(i) + "_";
                    YaoOutputFileName += "seq_" + to_string(j);
                    YaoOutputFileName += "_otherparty_";
                    YaoOutputFileName += to_string(i); 
                    YaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                    
                    yaoOutputFile.open(YaoOutputFileName);
                    yaoOutputFile << decrypt_yaoResult;
                    yaoOutputFile.close();
                }
            }

            cout << "EVALUATOR OTHER SENDING..." << endl;
            // send other elements
            for(int restOfParties = 0; restOfParties < numOfParties; restOfParties++)
            {
                int numOfInputsRestOfParties = this->numOfInputsOtherParties[restOfParties];

                if(restOfParties != i && restOfParties != partyNum)
                {
                    for(int j = 0; j < numOfInputs; j++)
                    {
                        for(int k = 0; k < numOfInputsRestOfParties; k++)
                        {
                            std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                            newYaoOutputFileName += "otherparty_";
                            newYaoOutputFileName += to_string(restOfParties); 
                            newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";

                            ifstream yaoOutput(newYaoOutputFileName);
                            std::string yaoResult;
                            std::getline(yaoOutput, yaoResult);

                            // Encrypt and send
                            std::string encrypted_yaoResult;
                            encrypted_yaoResult = encryptString(this->cumulative_qkd_buffer[i], yaoResult);
                            channel->writeWithSize(encrypted_yaoResult);
                        }
                    }
                }
            }

            // Receive rest of parties
            for(int restOfParties = 0; restOfParties < numOfParties; restOfParties++)
            {
                int numOfInputsRestOfParties = this->numOfInputsOtherParties[restOfParties];
                if(restOfParties != partyNum && restOfParties != i)
                {
                    for(int j = 0; j < numOfInputsOtherParty; j++)
                    {
                        for(int k = 0; k < numOfInputsRestOfParties; k++)
                        {

                            // Initialize
                            string yaoResult;
                            string decrypt_yaoResult;
                            vector<byte> raw_yaoResult;

                            // Receive from channel
                            channel->readWithSizeIntoVector(raw_yaoResult);

                            // From vector to string
                            const byte * uc = &(raw_yaoResult[0]);
                            yaoResult = string(reinterpret_cast<char const *>(uc), raw_yaoResult.size());

                            // Decrypt
                            decrypt_yaoResult = decryptString(this->cumulative_qkd_buffer[i], yaoResult);
                            
                            // save to file
                            ofstream yaoOutputFile;

                            std::string YaoOutputFileName = "results/out_party_" + to_string(i) + "_";
                            YaoOutputFileName += "seq_" + to_string(j);
                            YaoOutputFileName += "_otherparty_";
                            YaoOutputFileName += to_string(restOfParties); 
                            YaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                            
                            yaoOutputFile.open(YaoOutputFileName);
                            yaoOutputFile << decrypt_yaoResult;
                            yaoOutputFile.close();
                        }    
                    }
                }
            }




        } else if(i > partyNum) {

            int myPort = ports[partyNum] + i*10 - 10;
            int otherPort = ports[i] + partyNum*10;

            
            cout <<"RECEIVE RESULTS"<<endl;
            me = SocketPartyData(boost_ip::address::from_string(ips[partyNum]), myPort);
            cout<<"my port = "<<myPort<<endl;
            other = SocketPartyData(boost_ip::address::from_string(ips[i]), otherPort);
            cout<<"other port = "<<otherPort<<endl;

            shared_ptr<CommParty> channel = make_shared<CommPartyTCPSynced>(io_service, me, other);
            // connect to party i
            channel->join(500, 5000);
            cout<<"channel established"<<endl;


            cout << "GARBLER FIRST RECEIVING..." << endl;
            // Receive internal results
            for(int j = 0; j < numOfInputsOtherParty; j++)
            {
                for(int k = j + 1; k < numOfInputsOtherParty; k++)
                {
                    // Initialize
                    string yaoResult;
                    string decrypt_yaoResult;
                    vector<byte> raw_yaoResult;
                    
                    // Receive from channel
                    channel->readWithSizeIntoVector(raw_yaoResult);
                    
                    // From vector to string
                    const byte * uc = &(raw_yaoResult[0]);
                    yaoResult = string(reinterpret_cast<char const *>(uc), raw_yaoResult.size());

                    // Decrypt
                    decrypt_yaoResult = decryptString(this->cumulative_qkd_buffer[i], yaoResult);

                    // save to file
                    ofstream yaoOutputFile;

                    std::string YaoOutputFileName = "results/out_party_" + to_string(i) + "_";
                    YaoOutputFileName += "seq_" + to_string(j);
                    YaoOutputFileName += "_otherparty_";
                    YaoOutputFileName += to_string(i); 
                    YaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                    
                    yaoOutputFile.open(YaoOutputFileName);
                    yaoOutputFile << decrypt_yaoResult;
                    yaoOutputFile.close();
                }
            }

            cout << "GARBLER SENDING INTERNAL RESULTS..." << endl;
            // Send internal results
            for(int j = 0; j < numOfInputs; j++)
            {
                for(int k = j + 1; k < numOfInputs; k++)
                {

                    std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                    newYaoOutputFileName += "otherparty_";
                    newYaoOutputFileName += to_string(partyNum); 
                    newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";

                    ifstream yaoOutput(newYaoOutputFileName);
                    std::string yaoResult;
                    std::getline(yaoOutput, yaoResult);


                    // Encrypt and send
                    // Note: type of internal computation is int. Thus, we need to compute encryption differently
                    std::string encrypted_yaoResult;
                    unsigned int encrypted_yaoResult_uint32;
                    unsigned int yaoResult_int = (unsigned int)std::stoi(yaoResult);

                    encrypted_yaoResult_uint32 = encrypt32bits(this->cumulative_qkd_buffer[i], yaoResult_int); // cipher function = decipher function
                    encrypted_yaoResult = bitset<32>(encrypted_yaoResult_uint32).to_string();

                    channel->writeWithSize(encrypted_yaoResult);

                }
            }

            cout << "GARBLER SECOND RECEIVING..." << endl;
            // Receive rest of parties
            for(int restOfParties = 0; restOfParties < numOfParties; restOfParties++)
            {
                int numOfInputsRestOfParties = this->numOfInputsOtherParties[restOfParties];
                
                if(restOfParties != partyNum && restOfParties != i)
                {
                    for(int j = 0; j < numOfInputsOtherParty; j++)
                    {
                        for(int k = 0; k < numOfInputsRestOfParties; k++)
                        {
                            // Initialize
                            string yaoResult;
                            string decrypt_yaoResult;
                            vector<byte> raw_yaoResult;

                            // Receive from channel
                            channel->readWithSizeIntoVector(raw_yaoResult);
                            
                            // From vector to string
                            const byte * uc = &(raw_yaoResult[0]);
                            yaoResult = string(reinterpret_cast<char const *>(uc), raw_yaoResult.size());

                            // Decrypt
                            decrypt_yaoResult = decryptString(this->cumulative_qkd_buffer[i], yaoResult);
                            
                            // save to file
                            ofstream yaoOutputFile;

                            std::string YaoOutputFileName = "results/out_party_" + to_string(i) + "_";
                            YaoOutputFileName += "seq_" + to_string(j);
                            YaoOutputFileName += "_otherparty_";
                            YaoOutputFileName += to_string(restOfParties); 
                            YaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";
                            
                            yaoOutputFile.open(YaoOutputFileName);
                            yaoOutputFile << decrypt_yaoResult;
                            yaoOutputFile.close();
                        }    
                    }
                }
            }

            // send other elements
            for(int restOfParties = 0; restOfParties < numOfParties; restOfParties++)
            {
                int numOfInputsRestOfParties = this->numOfInputsOtherParties[restOfParties];

                if(restOfParties != partyNum && restOfParties != i)
                {
                    for(int j = 0; j < numOfInputs; j++)
                    {
                        for(int k = 0; k < numOfInputsRestOfParties; k++)
                        {
                        
                            std::string newYaoOutputFileName = "results/out_myseq_" + to_string(j) + "_";
                            newYaoOutputFileName += "otherparty_";
                            newYaoOutputFileName += to_string(restOfParties); 
                            newYaoOutputFileName += "_otherseq_" + to_string(k) + ".txt";

                            ifstream yaoOutput(newYaoOutputFileName);
                            std::string yaoResult;
                            std::getline(yaoOutput, yaoResult);

                            // Encrypt and send
                            std::string encrypted_yaoResult;
                            encrypted_yaoResult = encryptString(this->cumulative_qkd_buffer[i], yaoResult);
                            channel->writeWithSize(encrypted_yaoResult);
                        }
                    }
                }
            }




        }

    }

}

//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //

//                                                      Auxiliary functions


string preprocessInput(string path)
{
    
    int numOfDigits = 0;
    string sequence;
    string element;

    std::string line;    
    ifstream inputFile(path);

    string A = "00";
    string C = "01";
    string G = "10";
    string T = "11";

    while(std::getline(inputFile, line))
    {
        ++numOfDigits;
        element += line;

        if(numOfDigits == 2)
        {
            if(element == A)
                sequence += "A";
            if(element == C)
                sequence += "C";
            if(element == G)
                sequence += "G";
            if(element == T)
                sequence += "T";
            
            numOfDigits = 0;
            element = "";

        }

    }

    return sequence;

}


float dissimilarity(string input_a, string input_b)
{

    // int hamDist = 0;
    // int length = input_a.length();
    int LEN_SEQ = 4000; // Same as int used in Boolean circuit
 
    int distance = 0;
    int total = 0;
    
    for(int i=0; i < LEN_SEQ; i++)
    {

        string sub_input_a = input_a.substr(i*8, 8);
        string sub_input_b = input_b.substr(i*8, 8);

        int count_a = (sub_input_a == "AAAAAAAA") ? 0 : 1;
		int count_b = (sub_input_b == "AAAAAAAA") ? 0 : 1;

        if(count_a && count_b){
			int count_a_xor_b = hammingDistance(sub_input_a, sub_input_b);			
			if(count_a_xor_b == 1)
			{
				distance = distance + 1;
			}
			total = total + 8;
			
		}
    }

	float dissimilarity = (distance > 0) ? (float) total/distance : 0;

    return dissimilarity;

}


int hammingDistance(string input_i, string input_j)
{

    int hamDist = 0;

    int length;
    length = input_i.length();
    
    
    for(int i=0; i < length; i++)
    {
        if(input_i[i] != input_j[i])
            hamDist++;
    }

    return hamDist;
}

unsigned int encrypt32bits(vector<unsigned char>& cumulative_qkd_buffer, unsigned int msg)
{
    
    unsigned int encrypted_msg;

    // Building key
    char a = cumulative_qkd_buffer[0];
    char b = cumulative_qkd_buffer[1];
    char c = cumulative_qkd_buffer[2];
    char d = cumulative_qkd_buffer[3];

    unsigned int encryption_key = a | (b<<8) | (c<<16) | (d<<24);
    cout << "Encryption key being used: " << encryption_key << endl;
    encrypted_msg= msg ^ encryption_key;

    vector<unsigned char>::iterator begin_it, end_it;
    begin_it = cumulative_qkd_buffer.begin();
    end_it = begin_it + 4;
    cumulative_qkd_buffer.erase(begin_it, end_it);

    return encrypted_msg;
}

string encryptString(vector<unsigned char>& cumulative_qkd_buffer, string yaoResult)
{

    // Initialize
    string encrypted_yaoResult;
    unsigned int encrypted_yaoResult_uint32;

    // Parse
    bitset<32> yaoResult_bitset(yaoResult);
    unsigned int yaoResult_int = (unsigned int)(yaoResult_bitset.to_ulong());

    // Encrypt
    encrypted_yaoResult_uint32 = encrypt32bits(cumulative_qkd_buffer, yaoResult_int); // cipher function = decipher function
    encrypted_yaoResult = bitset<32>(encrypted_yaoResult_uint32).to_string();

    return encrypted_yaoResult;
}

string decryptString(vector<unsigned char>& cumulative_qkd_buffer, string yaoResult)
{
    return encryptString(cumulative_qkd_buffer, yaoResult);
}





//

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% //
