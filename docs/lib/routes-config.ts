// for page navigation & to sort on leftbar

export type EachRoute = {
  title: string;
  href: string;
  noLink?: true;
  items?: EachRoute[];
};

export const ROUTES: EachRoute[] = [
  {
    title: "Getting Started",
    href: "/getting-started",
    noLink: true,
    items: [
      { title: "Introduction", href: "/introduction" },
      { title: "Installation", href: "/installation" },
      /*
      {
        title: "Installation",
        href: "/installation",
        items: [
          { title: "Laravel", href: "/laravel" },
          { title: "React", href: "/react" },
          { title: "Gatsby", href: "/gatsby" },
        ],
      },
      */
    ],
  },
  {
    title: "State Machines",
    href: "/state-machines",
    noLink: true,
    items: [
      { title: "Deterministic Finite Automaton", href: "/dfa" },
      { title: "Nondeterministic Finite Automaton", href: "/nfa" },
      { title: "Pushdown Automaton", href: "/pda" },
      { title: "Linear Bounded Automaton", href: "/lba" },
      { title: "Turing Machine", href: "/tm" },
    ],
  },
  {
    title: "Grammars",
    href: "/grammars",
    noLink: true,
    items: [
      { title: "Grammar", href: "/grammar" },
    ],
  },
  {
    title: "Regular Expression",
    href: "/regular-expression",
    noLink: true,
    items: [
      { title: "Regex", href: "/regex" },
    ],
  },
];

type Page = { title: string; href: string };

function getRecurrsiveAllLinks(node: EachRoute) {
  const ans: Page[] = [];
  if (!node.noLink) {
    ans.push({ title: node.title, href: node.href });
  }
  node.items?.forEach((subNode) => {
    const temp = { ...subNode, href: `${node.href}${subNode.href}` };
    ans.push(...getRecurrsiveAllLinks(temp));
  });
  return ans;
}

export const page_routes = ROUTES.map((it) => getRecurrsiveAllLinks(it)).flat();
