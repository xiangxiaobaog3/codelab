#include <iostream>

extern "C" {
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"
}

class Lua_State
{
    lua_State *L;
    public:
    Lua_State() : L(lua_open()) {}
    ~Lua_State() {
        lua_close(L);
    }

    // implicitly act as a lua_State pointer
    inline operator lua_State *() {
        return L;
    }
};

static void open_libs(lua_State *L) 
{
    luaopen_io(L);
    luaopen_base(L);
    luaopen_table(L);
    luaopen_string(L);
    luaopen_math(L);
    // luaopen_loadlib(L);
}


static int execute_program(lua_State *L)
{
    // make a short function to make program behaviour more clear
    return lua_pcall(L, 0, LUA_MULTRET, 0);
}


static void report_errors(lua_State *L, const int status)
{
    if (status != 0) 
    {
        std::cerr << "-- " << lua_tostring(L, -1) << std::endl;
        lua_pop(L, 1); // remove error message
    }
}

int main(int argc, char** argv)
{
    for (int n=1; n<argc; ++n)
    {
        Lua_State L;
        open_libs(L);
        int s = luaL_loadfile(L, argv[n]);

        if (s==0) 
            s = execute_program(L);
        report_errors(L, s);
        // lua_close(L) automatically called here
    }
    return 0;

}
