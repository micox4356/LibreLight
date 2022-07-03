
import time

import unittest
import _LibreLightDesk as desk

print()
print()
print()
print()
print()
print()
print("--TEST--")
print()
print()

class Test_Fixture(unittest.TestCase):
    def test_wing(self):
        print("test_wing")
        fix=[1,2,3,10,11,12]
        wing_buffer=desk.process_wings(fix)
        self.assertEqual(wing_buffer,[[1,2,3],[12,11,10]])

        desk.fx_prm["WING"] = 1
        wing_buffer=desk.process_wings(fix)
        self.assertEqual(wing_buffer,[fix])

        desk.fx_prm["WING"] = 0
        wing_buffer=desk.process_wings(fix)
        self.assertEqual(wing_buffer,[fix])

        desk.fx_prm["WING"] = -2
        wing_buffer=desk.process_wings(fix)
        self.assertEqual(wing_buffer,[fix])


    def _select(self):
        print("_select")
        fix = []
        for f in desk.FIXTURES.fixtures:
            #print("-",f)
            fix.append(f)
            desk.FIXTURES.select(fix=f,attr="RED",mute=1)
            desk.FIXTURES.select(fix=f,attr="GREEN",mute=1)
            #desk.FIXTURES.select(fix=f,attr="BLUE",mute=1)
        return fix

    def test_fix_select(self):
        print("test_fix_select")
        fix = self._select()
        self.assertEqual(len(fix),72)

        fix2 = desk.FIXTURES.get_active()
        self.assertTrue(fix)

    def test_fix_clear(self):
        print("test_fix_clear")
        fix = self._select()
        self.assertTrue(len(fix))

        desk.FIXTURES.clear()

        fix = desk.FIXTURES.get_active()
        self.assertTrue(len(fix))
         
    def test_gui_fixture_effect(self):
        print("test_guo_fixtures_effect")
        #print(desk.FIXTURES.fixtures.keys)
        fix = self._select()

        desk.modes.val("BLIND",1)
        wing_buffer=[fix]
                 
        #print(dir(desk.FIXTURES))
        #jdata =desk.process_effect(wing_buffer,fx_name="COSINUS")
        desk.fx_prm["SPEED"] = 200
        jdata =desk.process_effect(wing_buffer,fx_name="COS")

        x=desk.FIXTURES.fx_get() #fix=fix[0])
        print("x",len(x))

        time.sleep(.2)
        desk.FIXTURES.fx_off("all") #fix=fix[0])


        x=desk.FIXTURES.fx_get() #fix=fix[0])
        print("x",len(x))


class Test_Desk(unittest.TestCase):
    def test_file_list(self):
        base = desk.Base()
        _list = base._list()
        for i in _list: 
            print(i)
        self.assertTrue(len(_list))

if __name__ == "__main__":
    unittest.main()





