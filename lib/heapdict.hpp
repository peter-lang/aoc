#include <map>
#include <vector>
#include <tuple>
#include <functional>

template <class K, class V>
struct heapdict {

  typedef std::tuple<K, V, size_t> ITEM;

  std::map<K, ITEM> _map;
  std::vector<std::reference_wrapper<ITEM>> _heap;

  V value_at(size_t pos) {
    return std::get<1>(_heap[pos].get());
  }

  void _heap_item_descend(size_t pos) {
    while (true) {
      size_t smallest = pos;
      size_t left = 2*pos+1;
      size_t right = 2*pos+2;
      if (left < _heap.size() && value_at(left) < value_at(smallest)) {
        smallest = left;
      }
      if (right < _heap.size() && value_at(right) < value_at(smallest)) {
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

  void _heap_item_ascend(size_t pos) {
    while (pos > 0 && value_at(pos) < value_at((pos-1)/2)) {
      swap(pos, (pos-1)/2);
      pos = (pos-1)/2;
    }
  }

  void swap(size_t a, size_t b) {
    std::swap(std::get<2>(_heap[a].get()), std::get<2>(_heap[b].get()));
    std::swap(_heap[a], _heap[b]);
  }

  std::tuple<K, V> pop_last() {
      const ITEM& item = _heap.back().get();
      auto result = make_tuple(std::get<0>(item), std::get<1>(item));
      _map.erase(std::get<0>(item));
      _heap.pop_back();
      return result;
  }

  std::tuple<K, V> pop_item(size_t pos = 0) {
    if (pos == _heap.size() - 1) {
      return pop_last();
    }
    // swap with last item to safely remove it
    swap(pos, _heap.size()-1);
    auto result = pop_last();
    // descend the last item to its real position
    _heap_item_descend(pos);
    return result;
  }

  size_t size() {
    return _heap.size();
  }

  void push_item(K key, V value) {
    auto found = _map.find(key);
    if (found != _map.end()) {
      ITEM& found_item = found->second;
      V& found_value = std::get<1>(found_item);
      if (found_value == value) {
        return;
      } else if (value > found_value) {
        found_value = value;
        // item get bigger, we can try to descend it
        _heap_item_descend(std::get<2>(found_item));
      } else {
        found_value = value;
        // item get smaller, we can try to ascend it
        _heap_item_ascend(std::get<2>(found_item));
      }
    } else {
      // add as last and ascend it
      size_t pos = _heap.size();
      auto item = std::make_tuple(key, value, pos);
      auto pair = _map.insert(std::pair<K, ITEM&>(key, item));
      _heap.emplace_back(pair.first->second);
      
      _heap_item_ascend(pos);
    }
  }
};
