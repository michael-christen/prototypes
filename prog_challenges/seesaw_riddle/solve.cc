#include <iostream>
#include <vector>
#include <cstdint>
#include <cassert>
#include <algorithm>
#include <cstring>


constexpr uint8_t kTotalNumObjects = 12;

struct State {
  int num_unknown, num_known, num_less, num_greater;

  uint32_t Id() const {
    if (num_unknown == 12) { 
      return 0;
    }
    return 1 * (num_unknown) + 12 * (num_known) + 144 * (num_less) + 1728 * (num_greater);
  }

  bool Done() const {
    return num_known == kTotalNumObjects - 1;
  }

  bool Valid() const {
    return num_known <= kTotalNumObjects - 1;
  }

  uint8_t Total() const { 
    return num_unknown + num_known + num_less + num_greater;
  }
};

struct Comparison {
  const State left, right;
};

std::vector<State> GetStates(const State& parent_state, const Comparison& comparison) {
  assert(comparison.left.Total() == comparison.right.Total());
  std::vector<State> results;
  const bool all_unknown = (comparison.left.num_unknown + comparison.left.num_known + comparison.right.num_unknown + comparison.right.num_known) == comparison.left.Total() * 2;
  const int unknown_total =  comparison.left.num_unknown + comparison.right.num_unknown;
  const int less_total =  comparison.left.num_less + comparison.right.num_less;
  const int greater_total =  comparison.left.num_greater + comparison.right.num_greater;
  const int unknown_excluded = parent_state.num_unknown - unknown_total;
  const int less_excluded = parent_state.num_less - less_total;
  const int greater_excluded = parent_state.num_greater - greater_total;
  // ==
  // everything inside this must be known
  {
    // What wasn't tested are all that remains unknown
    State eq_state({
      .num_unknown = parent_state.num_unknown - unknown_total,
      .num_known = parent_state.num_known + unknown_total + less_total + greater_total,
      .num_less = parent_state.num_less - less_total,
      .num_greater = parent_state.num_greater - greater_total,
    });
    if (eq_state.Valid() ) {
      results.push_back(eq_state);
    }
  }
  // >
  // anything on left that was less is now known
  // anything on right that was greater is now known
  // anything on left that was greater is still unknown
  // anything on right that was less is still unknown
  // what if left side is all
  // '' less
  // (still must remain some unknown)
  // '' greater
  // '' known
  // '' unknown
  // XXX: Does each individual need a history?
  // anything not in this is now known
  // Can't have all items be known
  if(all_unknown || (comparison.left.num_greater > 0 || comparison.right.num_less > 0)) {

    State greater_state({
      .num_unknown = parent_state.num_unknown -
        comparison.left.num_unknown - comparison.right.num_unknown - unknown_excluded,
      .num_known = parent_state.num_known + comparison.left.num_less +
        comparison.right.num_greater + unknown_excluded + greater_excluded +
        less_excluded,
      .num_less = parent_state.num_less - comparison.left.num_less +
        comparison.right.num_unknown - less_excluded,
      .num_greater = parent_state.num_greater - comparison.right.num_greater +
        comparison.left.num_unknown - greater_excluded,
    });
    if (greater_state.Valid()) {
      results.push_back(greater_state);
    }
  }
  // <
  if(all_unknown || (comparison.right.num_greater > 0 || comparison.left.num_less > 0)) {
    State lesser_state({
      .num_unknown = parent_state.num_unknown -
        comparison.right.num_unknown - comparison.left.num_unknown - unknown_excluded,
      .num_known = parent_state.num_known + comparison.right.num_less +
        comparison.left.num_greater + unknown_excluded + greater_excluded +
        less_excluded,
      .num_less = parent_state.num_less - comparison.right.num_less +
        comparison.left.num_unknown - less_excluded,
      .num_greater = parent_state.num_greater - comparison.left.num_greater +
        comparison.right.num_unknown - greater_excluded,
    });
    if (lesser_state.Valid()) {
      results.push_back(lesser_state);
    }
  }
  return results;
};

std::ostream& operator<<(std::ostream& os, const State& obj) {
  os << (unsigned)obj.num_unknown << "," << (unsigned)obj.num_known << "," <<
    (unsigned)obj.num_less << "," << (unsigned)obj.num_greater;
  return os;
}

std::ostream& operator<<(std::ostream& os, const Comparison& obj) {
  os << obj.left << " vs " << obj.right;
  return os;
}

std::vector<State> GetPossibleStates(const State& state, int size) {
  std::vector<State> results;
  // Collect all groupings of size (possible_side_size) on each side, from
  // num_unkown, num_known, num_less, num_greater groups.
  for(uint8_t num_unknown = 0; num_unknown <= state.num_unknown; ++ num_unknown) {
    for(uint8_t num_known = 0; num_known <= state.num_known; ++ num_known) {
      for(uint8_t num_less = 0; num_less <= state.num_less; ++ num_less) {
        for(uint8_t num_greater = 0; num_greater <= state.num_greater; ++ num_greater) {
          // TODO: Reduce search space by breaking early, etc.
          State state({.num_unknown = num_unknown, .num_known = num_known, .num_less = num_less, .num_greater = num_greater});
          if (state.Total() == size) {
            results.push_back(state);
          }
        }
      }
    }
  }
  return results;
}

std::vector<State> GetRightStates(const State& state, const State& left_state) {
  int side_size = left_state.Total();
  State source {.num_unknown = state.num_unknown - left_state.num_unknown,
    .num_known = state.num_known - left_state.num_known,
    .num_less = state.num_less - left_state.num_less,
    .num_greater = state.num_greater - left_state.num_greater};
  return GetPossibleStates(source, side_size);
}

std::vector<Comparison> GetAllComparisons(const State& state) {
  std::vector<Comparison> results;
  for(int possible_side_size = 1; possible_side_size <= kTotalNumObjects / 2; ++possible_side_size) {
    std::vector<State> lefts = GetPossibleStates(state, possible_side_size);
    for (const auto &left : lefts) {
      std::vector<State> rights = GetRightStates(state, left);
      for (const auto &right : rights) {
        // TODO: Remove duplicates
        results.push_back({.left = left, .right = right});
      }
    }
  }
  return results;
}


bool StateIdCheck (const State& a, const State& b) {
  return a.Id() == b.Id();
}


constexpr int kMaxDepth = 3;


void PrintPath(int depth, const State& state, int distance_to_valid_state[20736]) {
  if (depth > kMaxDepth + 1) {
    return;
  }
  std::string tab = "";
  for (int i = 0; i < depth; ++i) {
    tab += "  ";
  }
  std::cout << tab << state << std::endl;
  std::vector<Comparison> comparisons = GetAllComparisons(state);
  // TODO: Depth search
  std::vector<State> next_states;
  for(const auto & comparison : comparisons) {
    std::vector<State> states_from_comparison = GetStates(state, comparison);
    int distance = 0;
    for (const auto & comp_state : states_from_comparison) {
      distance = std::max(distance, distance_to_valid_state[comp_state.Id()]);
    }
    if (states_from_comparison.empty() || distance <= kMaxDepth - depth) {
      std::cout << tab << distance << " " << comparison << std::endl;
      for (const auto & comp_state : states_from_comparison) {
        PrintPath(depth + 1, comp_state, distance_to_valid_state);
      }
    } else {
      // std::cout << "Y " << distance << " " << kMaxDepth - depth << " " << comparison << std::endl;
    }
  }
}

// TODO: DFS
// TODO: Memoization
// Returns maximum distance to valid state
int Search(int depth, const std::vector<State> states, int distance_to_valid_state[20736]) {
  // Add visited
  if (depth > kMaxDepth) {
    bool all_done = true;
    for (const auto& state: states) { 
      if (!state.Done()) {
        all_done = false;
      }
    }
    if (all_done) { 
      return 0;
    } else {
      return 100;
    }
  }
  std::string tab = "";
  for (int i = 0; i < depth; ++i) {
    tab += "  ";
  }
  int max_distance = 0;
  for (const auto& state: states) { 
    if (state.Done()) {
      std::cout << tab << "X Search " << depth << " " << state << std::endl;
      continue;
    } else {
      std::cout << tab << "Search " << depth << "  " << state << std::endl;
    }
    std::vector<Comparison> comparisons = GetAllComparisons(state);
    // TODO: Depth search
    std::vector<State> next_states;
    int min_comparison_distance = 100;
    for(const auto & comparison : comparisons) {
      std::cout << tab << "    " << comparison << std::endl;
      std::vector<State> states_from_comparison = GetStates(state, comparison);
      for (const auto & next_state: states_from_comparison) { 
        std::cout << tab << "      " << next_state << std::endl;
      }
      if (state.Id() >= 20736) {
        std::cerr << state << " " << state.Id() << std::endl;
        assert(false);
      }
      min_comparison_distance = std::min(min_comparison_distance,
          1 + Search(depth + 1, states_from_comparison, distance_to_valid_state));

      // next_states.insert(next_states.end(), states_from_comparison.begin(), states_from_comparison.end());
    }
    max_distance = std::max(max_distance, min_comparison_distance);
    distance_to_valid_state[state.Id()] = std::min(
        distance_to_valid_state[state.Id()],
        max_distance);
    // std::unique(next_states.begin(), next_states.end(), StateIdCheck);
  }
  return max_distance;
}


int main() {
  State original_state({.num_unknown = kTotalNumObjects, .num_known = 0, .num_less = 0, .num_greater = 0});
  std::cout << original_state << std::endl;
  int distance_to_valid_state[20736];
  for (int i = 0; i < 20736; ++i) {
    distance_to_valid_state[i] = 100;
  }
  // Fill out search path
  std::cout << "Quickest path is " << Search(1, {original_state}, distance_to_valid_state) << std::endl;
  std::cout << "print path" << std::endl;
  PrintPath(1, original_state, distance_to_valid_state);
  // Walk shortest path (hopefully all)
  std::cout << "Done." << std::endl;
  return 0;
}
