// Seeds only addresses supported by MAME captures for Killer Instinct v1.5d.
//@category KillerInstinct

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;

public class SeedKi15d extends GhidraScript {

    private Address address(String value) throws Exception {
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(value);
    }

    private void seedCode(String value, String name, boolean function, boolean entry)
            throws Exception {
        Address target = address(value);
        if (!currentProgram.getMemory().contains(target)) {
            println("Skipping " + name + ": address not in this program");
            return;
        }
        disassemble(target);
        createLabel(target, name, true, SourceType.USER_DEFINED);
        if (entry) {
            currentProgram.getSymbolTable().addExternalEntryPoint(target);
        }
        if (function) {
            Function existing = getFunctionAt(target);
            if (existing == null) {
                existing = createFunction(target, name);
            }
            if (existing != null) {
                existing.setName(name, SourceType.USER_DEFINED);
            }
        }
        println("Seeded " + name + " at " + target);
    }

    @Override
    public void run() throws Exception {
        if (currentProgram == null) {
            throw new IllegalStateException("No program is open");
        }
        String language = currentProgram.getLanguageID().toString();
        if (!language.equals("MIPS:LE:64:64-32addr")) {
            throw new IllegalStateException("Unexpected language: " + language);
        }

        seedCode("bfc00000", "boot_reset_vector", false, true);
        seedCode("bfc00388", "boot_entry", true, true);

        seedCode("88000000", "loaded_vector", false, true);
        seedCode("880001b8", "loaded_entry", true, true);
        seedCode("8800034c", "jump_to_main_controller", false, false);
        seedCode("8800700c", "copy_record_fields", true, false);
        seedCode("88012614", "wait_vblank_cycle", true, false);
        seedCode("8802aa24", "main_controller", true, true);
        seedCode("8802ae14", "main_loop_head", false, false);
        seedCode("8802d5b0", "checksum_mix_step", true, false);
        seedCode("8802d5e0", "checksum_mix_step_x3", true, false);
    }
}
