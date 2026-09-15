use vergen_gix::{Build, Cargo, Emitter, Gix, Rustc, Sysinfo};

fn main() -> anyhow::Result<()> {
    let build = Build::all_build();
    let cargo = Cargo::all_cargo();
    let gix = Gix::all_git();
    let rustc = Rustc::all_rustc();
    let sysinfo = Sysinfo::all_sysinfo();

    Emitter::default()
        .add_instructions(&build)?
        .add_instructions(&cargo)?
        .add_instructions(&gix)?
        .add_instructions(&rustc)?
        .add_instructions(&sysinfo)?
        .emit()
}
