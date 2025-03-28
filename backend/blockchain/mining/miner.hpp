#ifndef MINER_HPP
#define MINER_HPP

#include <string>

std::pair<std::string, int> mine_block(const std::string& data, int difficulty);

#endif
