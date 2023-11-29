#include <fstream>
#include <iostream>
#include <random>
#include <utility>
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

  void positionRobotAndPackage() {
    std::vector<std::pair<int, int>> freeSpaces;
    for (int i = 0; i < rows; ++i) {
      for (int j = 0; j < cols; ++j) {
        if (map[i][j] == 0) {
          freeSpaces.emplace_back(i, j);
        }
      }
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, freeSpaces.size() - 1);

    // Randomly select two different positions for the robot and the package
    int index1 = distrib(gen);
    int index2 = distrib(gen);
    while (index1 == index2) {
      index2 = distrib(gen); // Ensure different positions
    }

    robotPos = freeSpaces[index1];
    packagePos = freeSpaces[index2];
  }

  void printRobotAndPackagePosition() {
    std::cout << "Robot Position: (" << robotPos.first << ", "
              << robotPos.second << ")\n";
    std::cout << "Package Position: (" << packagePos.first << ", "
              << packagePos.second << ")\n";
  }

private:
  int rows, cols;
  std::vector<std::vector<int>> map;
  std::pair<int, int> robotPos;
  std::pair<int, int> packagePos;
};

int main() {
  std::srand(static_cast<unsigned int>(time(nullptr)));

  Environment env(500, 500);
  env.saveToFile("../wharehouse_ex/500_500.csv");

  env.positionRobotAndPackage();
  env.printRobotAndPackagePosition();

  return 0;
}
