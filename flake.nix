{
  description = "A Nix-flake-based Shell development environment";

  inputs.nixpkgs.url = "github:Alper-Celik/nixpkgs/geckodriver-update";

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        f:
        nixpkgs.lib.genAttrs supportedSystems (
          system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
          }
        );
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default =
            let
              my-python = pkgs.python3;
              python-with-my-packages = my-python.withPackages (
                p: with p; [
                  selenium
                  ipython
                ]
              );
            in
            pkgs.mkShell {
              packages = with pkgs; [
                python-with-my-packages

                geckodriver
                firefox

                rclone
                unzip
              ];
            };
        }
      );
    };
}
