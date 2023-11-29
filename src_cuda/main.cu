#include <cfloat>
#include <cstdint>
#include <cuda_runtime.h>
#include <cuda_runtime_api.h>
#include <fstream>
#include <iostream>
// #include <limits>
#include <random>
#include <utility>
#include <vector>

// Node structure for A* algorithm
struct Node {
  int x, y; // Coordinates
  float gCost, hCost, fCost;
  Node *parent;

  // Constructor
  Node()
      : x(0), y(0), gCost(FLT_MAX), hCost(FLT_MAX), fCost(FLT_MAX),
        parent(nullptr) {}
};

__device__ float manhattanDistance(int x1, int y1, int x2, int y2) {
  return abs(x1 - x2) + abs(y1 - y2);
}

__global__ void initializeNodesKernel(Node *d_nodes, int rows, int cols) {
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  int idy = blockIdx.y * blockDim.y + threadIdx.y;

  if (idx < cols && idy < rows) {
    int index = idy * cols + idx;
    d_nodes[index].x = idx;
    d_nodes[index].y = idy;
    d_nodes[index].gCost = FLT_MAX;
    d_nodes[index].hCost = FLT_MAX;
    d_nodes[index].fCost = FLT_MAX;
    d_nodes[index].parent = nullptr;
  }
}

__global__ void aStarKernel(Node *d_nodes, int rows, int cols, int targetX,
                            int targetY) {
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  int idy = blockIdx.y * blockDim.y + threadIdx.y;

  if (idx < cols && idy < rows) {
    int index = idy * cols + idx;
    d_nodes[index].x = idx;
    d_nodes[index].y = idy;
    d_nodes[index].gCost = FLT_MAX;
    d_nodes[index].hCost = manhattanDistance(idx, idy, targetX, targetY);
    d_nodes[index].fCost = FLT_MAX;
    d_nodes[index].parent = nullptr;
  }
}

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
  // Environment(int rows, int cols) : rows(rows), cols(cols) {
  //   map.resize(rows, std::vector<int>(cols, 0));
  //   createWithPatterns();
  // }
  std::pair<int, int> robotPos;
  std::pair<int, int> packagePos;

  Environment(int rows, int cols) : rows(rows), cols(cols) {
    map.resize(rows, std::vector<int8_t>(cols, 0));
    nodeGrid.resize(rows, std::vector<Node>(cols));
    createWithPatterns();
    initializeNodes();
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

  void initializeNodes() {
    for (int i = 0; i < rows; i++) {
      for (int j = 0; j < cols; j++) {
        nodeGrid[i][j].x = i;
        nodeGrid[i][j].y = j;
      }
    }
  }

private:
  int rows, cols;
  std::vector<std::vector<Node>> nodeGrid;
  std::vector<std::vector<int8_t>> map;
};

int main() {
  std::srand(static_cast<unsigned int>(time(nullptr)));

  Environment env(500, 500);
  env.saveToFile("../../wharehouse_ex/500_500.csv");

  env.positionRobotAndPackage();
  env.printRobotAndPackagePosition();

  int rows = 500;
  int cols = 500;
  size_t size = rows * cols * sizeof(Node);

  Node *d_nodes;
  cudaMalloc(&d_nodes, size);

  // Assuming a block size of 16x16, adjust as necessary
  dim3 dimBlock(16, 16);
  dim3 dimGrid((cols + dimBlock.x - 1) / dimBlock.x,
               (rows + dimBlock.y - 1) / dimBlock.y);

  initializeNodesKernel<<<dimGrid, dimBlock>>>(d_nodes, rows, cols);

  cudaDeviceSynchronize();

  int targetX = env.packagePos.first;
  int targetY = env.packagePos.second;

  aStarKernel<<<dimGrid, dimBlock>>>(d_nodes, rows, cols, targetX, targetY);
  cudaDeviceSynchronize();

  cudaFree(d_nodes);

  return 0;
}
