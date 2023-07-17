#include "runtime.h"
#include "utils.h"
#include "utils_assert.h"

static foo_Instance_t foo_instance_foo1;
static foo_Instance_t foo_instance_foo2;
/* Begin User Code Section: Declarations */

/* End User Code Section: Declarations */
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
    /* Begin User Code Section: bar/write:write Start */

    /* End User Code Section: bar/write:write Start */
    bar_write_variable = value;
    bar_write_queue_overflow = bar_write_queue_data_valid;
    bar_write_queue = value;
    bar_write_queue_data_valid = true;
    bar_write_queue1_overflow = bar_write_queue1_data_valid;
    bar_write_queue1 = value;
    bar_write_queue1_data_valid = true;
    /* Begin User Code Section: bar/write:write End */

    /* End User Code Section: bar/write:write End */
}

void foo_Write_write(foo_Instance_t* instance, uint32_t value)
{
    /* Begin User Code Section: foo/write:write Start */

    /* End User Code Section: foo/write:write Start */
    if (instance == &foo_instance_foo1)
    {
        foo1_write_variable = value;
    }
    /* Begin User Code Section: foo/write:write End */

    /* End User Code Section: foo/write:write End */
}

uint32_t bar_Read_read(void)
{
    /* Begin User Code Section: bar/read:read Start */

    /* End User Code Section: bar/read:read Start */
    return foo1_write_variable;
    /* Begin User Code Section: bar/read:read End */

    /* End User Code Section: bar/read:read End */
}

uint32_t foo_Read_read(foo_Instance_t* instance)
{
    /* Begin User Code Section: foo/read:read Start */

    /* End User Code Section: foo/read:read Start */
    if (instance == &foo_instance_foo1)
    {
        return bar_write_variable;
    }
    /* Begin User Code Section: foo/read:read End */

    /* End User Code Section: foo/read:read End */
    return 0u;
}

QueueStatus_t foo_Read_read_queue(foo_Instance_t* instance, uint32_t* value)
{
    ASSERT(value != NULL);
    /* Begin User Code Section: foo/read_queue:read Start */

    /* End User Code Section: foo/read_queue:read Start */
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
    /* Begin User Code Section: foo/read_queue:read End */

    /* End User Code Section: foo/read_queue:read End */
    return QueueStatus_Empty;
}
