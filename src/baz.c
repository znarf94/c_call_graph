#include "foo.h"

static void baz_c();

void baz_a() {
    foo_b();
    baz_b();
    baz_c();
}

void baz_b() {
    foo_c();
    baz_c();
}

static void baz_c() {
}
