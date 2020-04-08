#include<memory>
#include<string>
#include<iostream>
#include<vector>

struct Node {
  std::string name;
  std::unique_ptr<Node> next;

  Node(std::string my_name): name(my_name) {}
};

class LinkedList {
  public:
    void Reinitialize(std::vector<std::string> names) {
      std::unique_ptr<Node> top = std::move(head_);
      while (top) {
        std::unique_ptr<Node> next_top = std::move(top->next);
        top.release();
        top = std::move(next_top);
      }
      Node* prev_node_ptr = nullptr;
      for (auto name : names) {
        std::unique_ptr<Node> this_node = std::make_unique<Node>(name);
        if (!prev_node_ptr) {
          head_ = std::move(this_node);
          prev_node_ptr = head_.get();
        } else {
          prev_node_ptr->next = std::move(this_node);
          prev_node_ptr = prev_node_ptr->next.get();
        }
      }
    }

    void Print() {
      Node* top = head_.get();
      int i = 0;
      while (top) {
        std::cout << i++ << ": " << top->name << std::endl;
        top = top->next.get();
      }
    };

    void Reverse() {
      std::unique_ptr<Node> prev_node = nullptr;
      std::unique_ptr<Node> cur_node = std::move(head_);
        std::unique_ptr<Node> next_node = nullptr;
      while (cur_node) {
        next_node = std::move(cur_node->next);
        cur_node->next = std::move(prev_node);
        if (!next_node) {
          head_ = std::move(cur_node);
          break;
        } else {
          prev_node = std::move(cur_node);
        }
        cur_node = std::move(next_node);
      }
    };

  private:
    std::unique_ptr<Node> head_ = nullptr;
};


int main() {
  LinkedList l;
  l.Reinitialize({"a", "b", "c"});
  l.Print();
  l.Reverse();
  l.Print();
}
