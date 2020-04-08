#include<iostream>
#include<chrono>
#include<thread>
#include<condition_variable>

::std::mutex cv_m;
::std::condition_variable cv;

template <typename T>
void mem_watcher(T *x) {
  ::std::unique_lock<::std::mutex> lk(cv_m);
  ::std::cout << x << ::std::endl;
  T last_x = *x;
  while(cv.wait_for(lk, ::std::chrono::seconds(1)) == ::std::cv_status::timeout) {
    if (last_x != *x) {
      ::std::cout << "- " << *x << ::std::endl;
	  last_x = *x;
	}
  }
  // Loop exit on event.
  ::std::cout << "I'm done" << ::std::endl;
}


int main() {
  int x = 0;

  ::std::cout << "Main thread" << ::std::endl;

  ::std::thread first(mem_watcher<int>, &x);
  for(;;) {
    ::std::cout << "Enter a value: ";
	::std::cin >> x;
	if (x == 3003) {
      break;
	}
  }
  ::std::cout << "Done, signalling!" << ::std::endl;
  cv.notify_all();
  first.join();
  ::std::cout << "Completed" << ::std::endl;
  return 0;
}
