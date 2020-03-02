#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;

void Runtime_RaiseEvent_OnInit(void)
{
    foo_Run_Runnable(&foo_instance_foo1, 5);
    foo_Run_Runnable(&foo_instance_foo2, 6);
}

void foo_Write_WPort(foo_Instance_t* instance, uint32_t value)
{
}

uint32_t foo_Read_RPort(foo_Instance_t* instance)
{
}
