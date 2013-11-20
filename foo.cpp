#include <cstdlib>

extern "C" {

void set_seed(size_t sed) {
    srand(sed);
}

size_t get_random() {
    return random();
}

char get_random_char() {
    return (char)(97 + random() % 26);
}

}



