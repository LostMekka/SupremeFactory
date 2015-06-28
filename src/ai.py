import sf_data.sf_module

class AI:
    
    def __init__(self, factory):
        self.factory = factory
        factory.get_module((0, 0)).set_target_dir(3, True)
        factory.get_module((2, 0)).set_target_dir(2, True)
        factory.get_module((0, 1)).set_target_dir(0, False)
        factory.get_module((0, 1)).set_target_dir(1, True)
        factory.get_module((1, 1)).set_target_dir(0, False)
        factory.get_module((2, 1)).set_target_dir(0, False)
        factory.get_module((3, 1)).set_target_dir(0, False)
        factory.get_module((3, 1)).set_target_dir(1, True)
        factory.get_module((3, 1)).set_target_dir(3, True)
        factory.get_module((0, 2)).set_target_dir(1, True)
        factory.get_module((2, 2)).set_target_dir(2, True)
        factory.get_module((3, 2)).set_target_dir(0, False)
        factory.get_module((3, 2)).set_target_dir(1, True)
        self.built_modules = []
        self.modules_for_lfe = []
        self.modules_for_dmg = []
        self.modules_for_rng = []
        self.modules_for_spd = []
        self.modules_for_gen = []
        self.modules_for_dmg.append(factory.get_module((0, 0)))
        self.modules_for_dmg.append(factory.get_module((1, 0)))
        self.modules_for_dmg.append(factory.get_module((2, 0)))
        self.dmgmodule = factory.get_module((3, 0))
        self.modules_for_rng.append(factory.get_module((0, 1)))
        self.modules_for_gen.append(factory.get_module((1, 1)))
        self.modules_for_gen.append(factory.get_module((2, 1)))
        self.modules_for_dmg.append(factory.get_module((3, 1)))
        self.lfemodule = factory.get_module((0, 2))
        self.modules_for_lfe.append(factory.get_module((1, 2)))
        self.modules_for_lfe.append(factory.get_module((2, 2)))
        self.modules_for_spd.append(factory.get_module((3, 2)))
        self.generators = []
        self.modules = []
        self.lists = [
                self.modules_for_lfe,
                self.modules_for_dmg,
                self.modules_for_rng,
                self.modules_for_spd,
        ]
    
    def update(self, time):
        # build the generators first!
        if len(self.modules_for_gen) > 0:
            gen = self.modules_for_gen.pop()
            if gen.can_build_new():
                gen.build_new(sf_data.sf_module.Module.type_generator)
                self.generators.append(gen)
            else:
                self.modules_for_gen.insert(0, gen)
            return
        # upgrade generators if possible
        if len(self.generators) > 0:
            gen = self.generators.pop()
            self.generators.insert(0, gen)
            if gen.can_upgrade():
                gen.upgrade()
                return
        # build other modules
        if len(lists) > 0:
            list = self.lists.pop()
            mod = list.pop()
            if mod.can_build_new():
                if list is self.modules_for_lfe: mod.build_new(sf_data.sf_module.Module.type_hp)
                if list is self.modules_for_dmg: mod.build_new(sf_data.sf_module.Module.type_attack)
                if list is self.modules_for_rng: mod.build_new(sf_data.sf_module.Module.type_range)
                if list is self.modules_for_spd: mod.build_new(sf_data.sf_module.Module.type_speed)
                self.modules.append(mod)
            else:
                list.insert(0, mod)
            if len(list) > 0:
                self.lists.insert(0, list)
            return
        # upgrade remaining modules
        if len(self.modules) > 0:
            mod = self.modules.pop()
            if mod.can_upgrade():
                mod.upgrade()
                if not mod.is_max_level():
                    self.modules.insert(0, mod)
                return
            self.modules.insert(0, mod)
        # nothing to do apparently. just cross fingers and hope the strat works
    