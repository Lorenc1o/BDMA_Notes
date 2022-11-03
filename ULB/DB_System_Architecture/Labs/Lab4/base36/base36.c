/*
 * Base36 PostgreSQL input/output function for bigint
 *
 */

#include <stdio.h>
#include "postgres.h"

#include "access/gist.h"
#include "access/skey.h"
#include "utils/elog.h"
#include "utils/palloc.h"
#include "utils/builtins.h"
#include "libpq/pqformat.h"
#include "utils/date.h"
#include "utils/datetime.h"
#include "utils/guc.h"
#include <sys/time.h>
#include <time.h>
#include <stdlib.h>
#include <ctype.h>


PG_MODULE_MAGIC;


#define BASE36_LENGTH      13

typedef long long int base36;

static int base36_digits[36] =
  {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
   'U', 'V', 'W', 'X', 'Y', 'Z'
  };

static base36 base36_powers[BASE36_LENGTH] = {
    1ULL,
    36ULL,
    1296ULL,
    46656ULL,
    1679616ULL,
    60466176ULL,
    2176782336ULL,
	78364164096ULL,
	2821109907456ULL,
	101559956668416ULL,
	3656158440062976ULL,
	131621703842267136ULL,
	4738381338321616896ULL
  };

static inline base36 base36_from_str(const char *str){
  //code
  base36 result = 0;
  int length = strlen(str);
  if(length > BASE36_LENGTH){
    elog(ERROR, "base36 string too long");
  }
  for(int i=0; i<length; i++){
    int digit = 0;
    if(str[i] == '\0'){
      break;
    }
    if(!isalnum(str[i])){
      elog(ERROR, "Invalid character in base36 string");
    }
    if(isdigit(str[i])){
      digit = str[i] - '0';
    }else{
      digit = toupper(str[i]) - 'A' + 10;
    }
    result += digit * base36_powers[length - i - 1];
  }
  return result;
}

static inline char* base36_to_str(base36 value){
  //code
  char *result = palloc(BASE36_LENGTH + 1);
  int digit = 0;
  for(int i=0; i<BASE36_LENGTH; i++){
    digit = value / base36_powers[BASE36_LENGTH - i - 1];
    result[i] = base36_digits[digit];
    value -= digit * base36_powers[BASE36_LENGTH - i - 1];
  }
  result[BASE36_LENGTH] = '\0';
  return result;
} 

Datum base36_encode(PG_FUNCTION_ARGS);

PG_FUNCTION_INFO_V1(base36_encode);
Datum base36_encode(PG_FUNCTION_ARGS){
    base36 num = PG_GETARG_INT64(0);
    PG_RETURN_CSTRING(base36_to_str(num));
}  

Datum base36_in(PG_FUNCTION_ARGS);

PG_FUNCTION_INFO_V1(base36_in);
Datum base36_in(PG_FUNCTION_ARGS){
    char *str = PG_GETARG_CSTRING(0);
    PG_RETURN_INT64(base36_from_str(str));
}   

PG_FUNCTION_INFO_V1(base36_out);
Datum base36_out(PG_FUNCTION_ARGS)
{
 base36 c = PG_GETARG_INT64(0);
 PG_RETURN_CSTRING(base36_to_str(c));
} 

PG_FUNCTION_INFO_V1(base36_recv);
Datum base36_recv(PG_FUNCTION_ARGS)
{
  StringInfo buf = (StringInfo) PG_GETARG_POINTER(0);
  const char *str = pq_getmsgstring(buf);
  pq_getmsgend(buf);
  PG_RETURN_INT64(base36_from_str(str));
}

PG_FUNCTION_INFO_V1(base36_send);
Datum base36_send(PG_FUNCTION_ARGS)
{
  base36 c = PG_GETARG_INT64(0);
  StringInfoData buf;

  pq_begintypsend(&buf);
  pq_sendstring(&buf, base36_to_str(c));

  PG_RETURN_BYTEA_P(pq_endtypsend(&buf));
}



