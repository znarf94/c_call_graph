#include "foo.h"
#include "baz.h"

void bar();

int main(void) {
    foo_a();
    baz_a();

    bar();

    if (0) {
        return 1;
    }

    return 0;
}
