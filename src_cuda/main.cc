#include <iostream>
#include <fstream>
#include <random>
#include <vector>

const int patternSize = 10;
const int numPatterns = 4;
int patterns[numPatterns][patternSize][patternSize] = {
    // pattern 1
    {{0, 0, 0, -1, 0, 0, -1, 0, 0, 0},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, 0, 0, -1, 0, 0, -1, 0, 0, -1},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, 0, 0, -1, 0, 0, -1, 0, 0, -1},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, 0, 0, -1, 0, 0, -1, 0, 0, -1}},
    // pattern 2
    {{0, 0, 0, -1, 0, 0, -1, 0, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {-1, 0, 0, -1, 0, 0, -1, 0, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {-1, 0, 0, -1, 0, 0, -1, 0, 0, 0},
     {0, 0, -1, 0, 0, -1, 0, 0, -1, 0},
     {0, -1, 0, 0, -1, 0, 0, -1, 0, 0},
     {-1, 0, 0, -1, 0, 0, -1, 0, 0, 0}},
    // pattern 3
    {{0, 0, 0, -1, 0, 0, 0, -1, 0, 0},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, -1, 0, -1, 0, -1, 0, -1},
     {0, -1, 0, 0, 0, -1, 0, 0, 0, -1}},
    // pattern 4
    {{0, -1, -1, -1, -1, 0, -1, -1, -1, -1},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
     {-1, -1, -1, -1, -1, 0, -1, -1, -1, 0},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
     {0, -1, -1, -1, -1, 0, -1, -1, -1, -1},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
     {-1, -1, -1, -1, -1, 0, -1, -1, -1, 0},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
     {0, -1, -1, -1, -1, 0, -1, -1, -1, -1},
     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}},
};

class Environment {
public:
  Environment(int rows, int cols) : rows(rows), cols(cols) {
    map.resize(rows, std::vector<int>(cols, 0));
    createWithPatterns();
  }

  void createWithPatterns() {
    for (int i = 0; i < rows; i += patternSize) {
      for (int j = 0; j < cols; j += patternSize) {
        // Choose a pattern and place it in the map
        int patternIndex = std::rand() % numPatterns; // Random pattern index
        for (int pi = 0; pi < patternSize && i + pi < rows; ++pi) {
          for (int pj = 0; pj < patternSize && j + pj < cols; ++pj) {
            map[i + pi][j + pj] = patterns[patternIndex][pi][pj];
          }
        }
      }
    }
  }

  void printMap() {
    for (const auto &row : map) {
      for (int cell : row) {
        std::cout << cell << " ";
      }
      std::cout << std::endl;
    }
  }

  void saveToFile(const std::string &filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
      std::cerr << "Failed to open file for writing." << std::endl;
      return;
    }

    for (const auto &row : map) {
      for (size_t j = 0; j < row.size(); ++j) {
        file << row[j];
        if (j < row.size() - 1)
          file << ",";
      }
      file << "\n";
    }
  }

private:
  int rows, cols;
  std::vector<std::vector<int>> map;
};

int main() {
  std::srand(static_cast<unsigned int>(time(nullptr)));

  Environment env(500, 500);
  env.saveToFile("file.txt");

  return 0;
}
