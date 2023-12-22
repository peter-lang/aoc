#include <map>
#include <vector>
#include <tuple>
#include <functional>
#include <memory>


template <class K, class V>
struct heapdict {

  typedef std::tuple<K, V, size_t> ITEM_VAL;
  typedef std::shared_ptr<ITEM_VAL> ITEM;

  std::map<K, ITEM> _map;
  std::vector<ITEM> _heap;

  void _heapify(size_t pos) {
    while (true) {
      size_t smallest = pos;
      size_t left = 2*pos+1;
      size_t right = 2*pos+2;
      if (left < _heap.size() && std::get<1>(*_heap[left]) < std::get<1>(*_heap[smallest])) {
        smallest = left;
      }
      if (right < _heap.size() && std::get<1>(*_heap[right]) < std::get<1>(*_heap[smallest])) {
        smallest = right;
      }
      if (smallest != pos) {
        swap(smallest, pos);
        pos = smallest;
      } else {
        break;
      }
    }
  }

  void swap(size_t a, size_t b) {
    std::swap(std::get<2>(*_heap[a]), std::get<2>(*_heap[b]));
    std::swap(_heap[a], _heap[b]);
  }

  std::tuple<K, V> pop_item(size_t pos = 0) {
    swap(pos, _heap.size()-1);
    const ITEM& item = _heap.back();
    _map.erase(std::get<0>(*item));
    auto result = make_tuple(std::get<0>(*item), std::get<1>(*item));
    _heap.pop_back();
    _heapify(pos);
    return result;
  }

  size_t size() {
    return _heap.size();
  }

  void push_item(K key, V value) {
    auto found = _map.find(key);
    if (found != _map.end()) {
      ITEM found_item = found->second;
      V& found_item_value = std::get<1>(*found_item);
      if (found_item_value == value) {
        return;
      } else if (value > found_item_value) {
        found_item_value = value;
        _heapify(std::get<2>(*found_item));
      } else {
        found_item_value = value;
        size_t pos = std::get<2>(*found_item);
        while (pos > 0 && std::get<1>(*_heap[pos]) < std::get<1>(*_heap[(pos-1)/2])) {
          swap(pos, (pos-1)/2);
          pos = (pos-1)/2;
        }
      }
    } else {
      size_t pos = _heap.size();
      auto item = std::make_shared<ITEM_VAL>(std::make_tuple(key, value, pos));
      _heap.push_back(item);
      _map.insert(std::pair<K, ITEM>(key, item));
      while (pos > 0 && std::get<1>(*_heap[pos]) < std::get<1>(*_heap[(pos-1)/2])) {
        swap(pos, (pos-1)/2);
        pos = (pos-1)/2;
      }
    }
  }
};
