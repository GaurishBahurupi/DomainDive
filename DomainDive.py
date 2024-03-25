import dns.resolver
import signal

class SubdomainFinder:
    def __init__(self, domain, subdomains_file):
        self.domain = domain
        self.subdomains_file = subdomains_file

    def discover_subdomains(self):
        print("Finding subdomains... This might take a while, grab a cup of coffee!")
        subdomains = set()

        try:
            with open(self.subdomains_file, 'r') as file:
                subdomain_list = file.read().splitlines()

            for subdomain in subdomain_list:
                full_subdomain = f"{subdomain}.{self.domain}"
                try:
                    signal.signal(signal.SIGALRM, self.handle_timeout)
                    signal.alarm(5)  # Timeout set to 5 seconds
                    answers = dns.resolver.resolve(full_subdomain, 'A')
                    subdomains.add(full_subdomain)
                    print(f"[+] Found subdomain: {full_subdomain}")
                except (dns.resolver.NXDOMAIN, dns.resolver.Timeout):
                    pass
                except BlockingIOError:
                    print("\nEncountered a temporary resource unavailability, skipping...")
                    continue
                except dns.resolver.NoAnswer:
                    pass
                finally:
                    signal.alarm(0)  # Cancel the alarm

            if subdomains:
                print("\n[+] Discovered subdomains:")
                for subdomain in subdomains:
                    print(subdomain)
            else:
                print("\nNo subdomains found.")
        except FileNotFoundError:
            print("Error: Subdomains file not found.")

    def handle_timeout(self, signum, frame):
        raise dns.resolver.Timeout()


def main():
    domain = input("Enter the domain to find subdomains: ")
    subdomains_file = "{path of subdomain_wordlist.txt}"  # Specify the path here
    finder = SubdomainFinder(domain, subdomains_file)
    finder.discover_subdomains()


if __name__ == "__main__":
    main()

