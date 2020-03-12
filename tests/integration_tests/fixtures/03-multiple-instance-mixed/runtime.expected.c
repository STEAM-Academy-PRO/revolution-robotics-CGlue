#include "runtime.h"
#include "utils.h"

static foo_Instance_t foo_instance_foo1;
static uint32_t foo1_write_variable = 0u;
static uint32_t bar_write_variable = 0u;

void bar_Write_write(uint32_t value)
{
    bar_write_variable = value;
}

void foo_Write_write(foo_Instance_t* instance, uint32_t value)
{
    if (instance == &foo_instance_foo1)
    {
        foo1_write_variable = value;
    }
}

uint32_t bar_Read_read(void)
{
    return foo1_write_variable;
}

uint32_t foo_Read_read(foo_Instance_t* instance)
{
    if (instance == &foo_instance_foo1)
    {
        return bar_write_variable;
    }
    return 0u;
}
