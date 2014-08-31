#include <stdio.h>

extern "C" {
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
}

/*  the lua interpreter */
lua_State* L;

static int pxxx(lua_State *L)
{
    int n = lua_gettop(L);
    const char* cstr = lua_tostring(L, 1);
    // char s[256] = lua_tostring(L, 1);
    int d = lua_tonumber(L, 2);
    lua_pushstring(L, cstr);
    return 2;
}

static int average(lua_State *L)
{
    /* get number of agruments */
    int n = lua_gettop(L);
    double sum = 0;
    int i;

    /* loop through each argument */
    for (i=1; i<=n; i++)
    {
        /* total the arguments */
        if (!lua_isnumber(L, i)) {
            lua_pushstring(L, "Incorrect argument to 'average'");
            lua_error(L);
        }
        sum += lua_tonumber(L, i);
    }

    /* push the average */
    lua_pushnumber(L, sum/n);

    /* push the sum */
    lua_pushnumber(L, sum);

    /* return the number of results */
    return 2;
}


int main (int argc, char *argv[])
{
    /* initialize Lua */
    L = lua_open();

    /* load Lua base libraries */
    luaL_openlibs(L);

    /* register our function */
    lua_register(L, "average", average);
    lua_register(L, "pxxx", pxxx);

    /* run the script */
    luaL_dofile(L, "avg.lua");

    /* cleanup Lua */
    lua_close(L);

    /* pause */
    printf("Press enter to exit...");
    getchar();
    return 0;
}
