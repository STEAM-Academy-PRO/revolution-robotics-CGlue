#ifndef COMPONENT_FOO_H_
#define COMPONENT_FOO_H_

#ifndef COMPONENT_TYPES_FOO_H_
#define COMPONENT_TYPES_FOO_H_

#include <stdint.h>


typedef struct {
    uint32_t var1;
} foo_Instance_t;
typedef void (*FuncPtr_t)(foo_Instance_t* instance);

typedef enum {
    QueueStatus_Empty,
    QueueStatus_Ok,
    QueueStatus_Overflow
} QueueStatus_t;

#endif /* COMPONENT_TYPES_FOO_H_ */

void foo_Run_Runnable(foo_Instance_t* instance, uint32_t arg1);
void foo_Run_FuncPtr(foo_Instance_t* instance);
void foo_Write_WIPort(foo_Instance_t* instance, uint32_t index, uint32_t value);
void foo_Write_WPort(foo_Instance_t* instance, uint32_t value);
uint32_t foo_Read_RIPort(foo_Instance_t* instance, uint32_t index);
uint32_t foo_Read_RPort(foo_Instance_t* instance);
uint32_t foo_Read_RPortFromI(foo_Instance_t* instance);
QueueStatus_t foo_Read_RQPort(foo_Instance_t* instance, uint32_t* value);

#endif /* COMPONENT_FOO_H_ */
