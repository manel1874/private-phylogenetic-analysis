#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>

int main()
{

    std::string file_path = "quantum_oblivious_key_distribution/signals/ok_1.txt ";
    std::ofstream file(file_path);

    // Write header:
    file << "SizeOKeys: 512" << std::endl;
    file << "NumberOKeys: 4" << std::endl;
    //std::ofstream file("test_ok_txt.txt");

    std::vector<char> okey_buffer;

    okey_buffer.push_back('\305');
    okey_buffer.push_back('\327');
    okey_buffer.push_back('\024');
    okey_buffer.push_back('\204');

    for(char key : okey_buffer)
    {
        std::string readable_key = std::bitset<8>(key).to_string();
        file << readable_key; 
    }

    file << std::endl;

        for(char key : okey_buffer)
    {
        std::string readable_key = std::bitset<8>(key).to_string();
        file << readable_key; 
    }

    file << std::endl;




    file.close();
    return 0;
}