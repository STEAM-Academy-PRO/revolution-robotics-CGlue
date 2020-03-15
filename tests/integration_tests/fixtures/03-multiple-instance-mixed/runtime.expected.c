#include "runtime.h"
#include "utils.h"
#include "utils_assert.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
static uint32_t foo1_write_variable = 0u;
static uint32_t bar_write_variable = 0u;
static uint32_t bar_write_queue;
static bool bar_write_queue_overflow = false;
static bool bar_write_queue_data_valid = false;
static uint32_t bar_write_queue1;
static bool bar_write_queue1_overflow = false;
static bool bar_write_queue1_data_valid = false;

void bar_Write_write(uint32_t value)
{
    bar_write_variable = value;
    bar_write_queue_overflow = bar_write_queue_data_valid;
    bar_write_queue = value;
    bar_write_queue_data_valid = true;
    bar_write_queue1_overflow = bar_write_queue1_data_valid;
    bar_write_queue1 = value;
    bar_write_queue1_data_valid = true;
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

QueueStatus_t foo_Read_read_queue(foo_Instance_t* instance, uint32_t* value)
{
    ASSERT(value != NULL);
    if (instance == &foo_instance_foo1)
    {
        bool was_overflow = bar_write_queue_overflow;
        if (bar_write_queue_data_valid)
        {
            bar_write_queue_overflow = false;
            *value = bar_write_queue;
            bar_write_queue_data_valid = false;
            if (was_overflow)
            {
                return QueueStatus_Overflow;
            }
            else
            {
                return QueueStatus_Ok;
            }
        }
    }
    if (instance == &foo_instance_foo2)
    {
        bool was_overflow = bar_write_queue1_overflow;
        if (bar_write_queue1_data_valid)
        {
            bar_write_queue1_overflow = false;
            *value = bar_write_queue1;
            bar_write_queue1_data_valid = false;
            if (was_overflow)
            {
                return QueueStatus_Overflow;
            }
            else
            {
                return QueueStatus_Ok;
            }
        }
    }
    return QueueStatus_Empty;
}
