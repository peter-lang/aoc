#include <type_traits>
#include <vector>
#include <cassert>

template <class T>
struct vec2 {
    T x, y;

    vec2(): x(0), y(0) {}
    vec2(T x, T y) : x(x), y(y) {}
    vec2(const vec2& v) : x(v.x), y(v.y) {}

    using SIGNED_T = typename std::make_signed<T>::type;

    SIGNED_T cmp(const vec2& v) const {
        SIGNED_T res = x - v.x;
        if (res != 0) {
            return res;
        }
        return y-v.y;
    }

    bool operator==(const vec2& v) const { return cmp(v) == 0; }
    bool operator!=(const vec2& v) const { return cmp(v) != 0; }
    bool operator<(const vec2& v) const { return cmp(v) < 0; }
    bool operator<=(const vec2& v) const { return cmp(v) <= 0; }
    bool operator>(const vec2& v) const { return cmp(v) > 0; }
    bool operator>=(const vec2& v) const { return cmp(v) >= 0; }

    vec2& operator=(const vec2& v) {
        x = v.x;
        y = v.y;
        return *this;
    }

    vec2 operator-() const { return vec2(-x, -y); }

    vec2 operator+(const vec2& v) const { return vec2(x + v.x, y + v.y); }

    vec2 operator-(const vec2& v) const { return vec2(x - v.x, y - v.y); }

    vec2& operator+=(const vec2& v) {
        x += v.x;
        y += v.y;
        return *this;
    }

    vec2& operator-=(const vec2& v) {
        x -= v.x;
        y -= v.y;
        return *this;
    }

    vec2 operator+(T s) const { return vec2(x + s, y + s); }

    vec2 operator-(T s) const { return vec2(x - s, y - s); }

    vec2 operator*(T s) const { return vec2(x * s, y * s); }

    vec2 operator/(T s) const { return vec2(x / s, y / s); }

    vec2& operator+=(T s) {
        x += s;
        y += s;
        return *this;
    }

    vec2& operator-=(T s) {
        x -= s;
        y -= s;
        return *this;
    }

    vec2& operator*=(T s) {
        x *= s;
        y *= s;
        return *this;
    }

    vec2& operator/=(T s) {
        x /= s;
        y /= s;
        return *this;
    }

    template <class U>
    operator vec2<U>() const {
        return vec2<U>(x, y);
    }
};

typedef vec2<int> vec2i;
typedef vec2<size_t> vec2size;

template <class T>
struct mx2;

template <class T>
struct mx2slice {
    vec2size shape;
    vec2size offset;
    mx2<T>& orig;

    const T& at(size_t x, size_t y) const {
        return orig.at(offset.x + x, offset.y + y);
    }

    T& at(size_t x, size_t y) {
        return orig.at(offset.x + x, offset.y + y);
    }

    const T& operator[](const vec2size& coord) const {
        return at(coord.x, coord.y);
    }

    T& operator[](const vec2size& coord) {
        return at(coord.x, coord.y);
    }

    mx2slice& operator+=(T s) {
        for (size_t x = 0; x < shape.x; x++)
            for (size_t y = 0; y < shape.y; y++)
                at(x, y) += s;
        return *this;
    }

    mx2slice& operator-=(T s) {
        for (size_t x = 0; x < shape.x; x++)
            for (size_t y = 0; y < shape.y; y++)
                at(x, y) -= s;
        return *this;
    }

    mx2slice& operator*=(T s) {
        for (size_t x = 0; x < shape.x; x++)
            for (size_t y = 0; y < shape.y; y++)
                at(x, y) *= s;
        return *this;
    }

    mx2slice& operator/=(T s) {
        for (size_t x = 0; x < shape.x; x++)
            for (size_t y = 0; y < shape.y; y++)
                at(x, y) /= s;
        return *this;
    }
};

template <class T>
struct mx2 {
    vec2size shape;
    std::vector<T> data;

    mx2(vec2size shape, const T& val = 0) : shape(shape), data(shape.x*shape.y, val) {}
    mx2(vec2size shape, const std::vector<T>& data) : shape(shape), data(data) {
        assert(data.size() == shape.x*shape.y);
    }
    mx2(const std::vector<std::vector<T>>& data2d) : mx2({data2d.size(), data2d[0].size()}) {
        for (int x = 0; x < shape.x; x++) {
            assert(data2d[x].size() == shape.y);
            std::copy(
                data2d[x].begin(),
                data2d[x].end(),
                data.begin() + x*shape.y
            );
        }
    }

    mx2(const mx2& v) : shape(v.shape), data(v.data) {}

    mx2& operator=(const mx2& v) {
        shape = v.shape;
        data = v.data;
        return *this;
    }

    size_t size() const {
        return data.size();
    }

    const T& at(size_t x, size_t y) const {
        return data[x*shape.y + y];
    }

    T& at(size_t x, size_t y) {
        return data[x*shape.y + y];
    }

    const T& operator[](const vec2size& coord) const {
        return at(coord.x, coord.y);
    }

    T& operator[](const vec2size& coord) {
        return at(coord.x, coord.y);
    }

    mx2 repeat(size_t x, size_t y) {
        mx2 result({shape.x*x, shape.y*y});
        size_t src_x_offset = y*shape.y;
        size_t rep_x_offset = shape.x*src_x_offset;
        for (size_t rep_x = 0; rep_x < x; rep_x++) {
            for (size_t src_x = 0; src_x < shape.x; src_x++) {
                for (size_t rep_y = 0; rep_y < y; rep_y++) {
                    std::copy(
                        data.begin()+src_x*shape.y,
                        data.begin()+(src_x+1)*shape.y,
                        result.data.begin()+rep_x*rep_x_offset + src_x*src_x_offset + rep_y*shape.y
                    );
                }
            }
        }
        return result;
    }

    mx2 operator-() const {
        mx2 result = *this;
        for (size_t i = 0; i < result.data.size(); i++) result.data[i] = -result.data[i];
        return result;
    }

    mx2 operator+(const mx2& v) const {
        mx2 result = *this;
        result += v;
        return result;
    }

    mx2 operator-(const mx2& v) const {
        mx2 result = *this;
        result -= v;
        return result;
    }

    mx2& operator+=(const mx2& v) {
        assert(shape == v.shape);
        for (size_t i = 0; i < data.size(); i++) data[i] += v.data[i];
        return *this;
    }

    mx2& operator-=(const mx2& v) {
        assert(shape == v.shape);
        for (size_t i = 0; i < data.size(); i++) data[i] -= v.data[i];
        return *this;
    }

    mx2 operator+(T s) const {
        mx2 result = *this;
        result += s;
        return result;
    }

    mx2 operator-(T s) const {
        mx2 result = *this;
        result -= s;
        return result;
    }

    mx2 operator*(T s) const {
        mx2 result = *this;
        result *= s;
        return result;
    }

    mx2 operator/(T s) const {
        mx2 result = *this;
        result /= s;
        return result;
    }

    mx2& operator+=(T s) {
        for (size_t i = 0; i < data.size(); i++) data[i] += s;
        return *this;
    }

    mx2& operator-=(T s) {
        for (size_t i = 0; i < data.size(); i++) data[i] -= s;
        return *this;
    }

    mx2& operator*=(T s) {
        for (size_t i = 0; i < data.size(); i++) data[i] *= s;
        return *this;
    }

    mx2& operator/=(T s) {
        for (size_t i = 0; i < data.size(); i++) data[i] /= s;
        return *this;
    }

    mx2slice<T> slice(vec2size shape, vec2size offset) {
        return {shape, offset, *this};
    }
};


