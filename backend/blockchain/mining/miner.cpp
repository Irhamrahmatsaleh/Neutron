#include "miner.hpp"
#include <iostream>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>

std::string sha256(const std::string& input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)input.c_str(), input.length(), hash);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i)
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];

    return ss.str();
}

std::pair<std::string, int> mine_block(const std::string& data, int difficulty) {
    int nonce = 0;
    std::string prefix(difficulty, '0');
    std::string hash;

    while (true) {
        std::string input = data + std::to_string(nonce);
        hash = sha256(input);
        if (hash.substr(0, difficulty) == prefix)
            break;
        ++nonce;
    }

    return {hash, nonce};
}

int main() {
    std::string data;
    int difficulty;

    std::getline(std::cin, data);
    std::cin >> difficulty;

    auto result = mine_block(data, difficulty);
    std::cout << result.first << " " << result.second << std::endl;

    return 0;
}
