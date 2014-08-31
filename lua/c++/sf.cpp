#ifndef __LUA_INC_H__
#define __LUA_INC_H__

extern "C" 
{
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}
#endif

int main(int argc, char** argv) 
{
    int iErr = 0;
    lua_State *lua = lua_open();
    luaopen_io(lua);
    luaL_openlibs(lua);

    if((iErr = luaL_loadfile(lua, "hello.lua")) == 0)
    {
        // push the function name onto the stack
        lua_pushstring(lua, "helloWorld");
        // Function is located in the Global Table
        lua_gettable(lua, LUA_GLOBALSINDEX);
        lua_pcall(lua, 0, 0, 0);

    }
    lua_close(lua);
}

