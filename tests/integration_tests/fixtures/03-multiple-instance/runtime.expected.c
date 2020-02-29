#include "runtime.h"

static foo_Instance_t foo_Instance_foo1;
static foo_Instance_t foo_Instance_foo2;

void Runtime_Run_OnInit(void)
{
    foo_Run_Runnable(&foo_Instance_foo1);
    foo_Run_Runnable(&foo_Instance_foo2);
}
