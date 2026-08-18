# GitHub Diffs

## ManishBisht777/portfolio

### Commit `4baeb1b20091fc5424ec6f0d6b101addf1412e6d`

**Message:** Merge pull request #8 from ManishBisht777/blog/building-automated-blog-generation

Blog/building automated blog generation

### `app/(portfolio)/blogs/[slug]/page.tsx`

```diff
@@ -0,0 +1,162 @@
+import Link from 'next/link';
+import PageFooter from '@/components/bookfolio/components/PageFooter';
+import { getBlogPost, getBlogSlugs, renderMarkdown } from '@/lib/blog';
+import { formatDate } from '@/utils/date';
+
+interface Props {
+  params: Promise<{ slug: string }>;
+}
+
+export async function generateStaticParams() {
+  const slugs = getBlogSlugs();
+  return slugs.map((slug) => ({ slug }));
+}
+
+export async function generateMetadata({ params }: Props) {
+  const { slug } = await params;
+  try {
+    const post = getBlogPost(slug);
+    return {
+      title: `${post.metadata.title} - Manish Bisht`,
+      description: post.metadata.description,
+    };
+  } catch {
+    return { title: 'Blog - Manish Bisht' };
+  }
+}
+
+export default async function BlogPostPage({ params }: Props) {
+  const { slug } = await params;
+
+  try {
+    const post = getBlogPost(slug);
+    const content = await renderMarkdown(post.content);
+
+    return (
+      <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+        <div>
+          <Link
+            href='/blogs'
+            className='text-[#876f90] hover:text-[#a087a0] transition-colors flex items-center gap-2 w-fit tracking-wider text-lg'
+          >
+            <span>←</span> Back to blogs
+          </Link>
+        </div>
+
+        <article className='flex flex-col gap-8'>
+          <div className='flex flex-col gap-4'>
+            <h1 className='text-5xl tracking-wider leading-tight md:text-6xl'>
+              {post.metadata.title}
+            </h1>
+            <div className='flex gap-4 text-muted-foreground tracking-wider text-lg flex-wrap'>
+              <span>{post.metadata.author || 'Manish Bisht'}</span>
+              <span>·</span>
+              <span>{formatDate(post.metadata.date)}</span>
+              <span>·</span>
+              <span>{post.metadata.reading_time || 5} min read</span>
+            </div>
+          </div>
+
+          <div
+            className='prose prose-invert max-w-none tracking-wider leading-relaxed'
+            style={{
+              '--tw-prose-body': 'var(--foreground)',
+              '--tw-prose-headings': 'var(--foreground)',
+              '--tw-prose-links': '#876f90',
+              '--tw-prose-code': 'var(--foreground)',
+            } as React.CSSProperties}
+          >
+            <style>{`
+              .prose h2 {
+                font-size: 1.875rem;
+                font-weight: 600;
+                margin-top: 3rem;
+                margin-bottom: 1.5rem;
+                letter-spacing: 0.05em;
+              }
+              .prose h3 {
+                font-size: 1.5rem;
+                font-weight: 500;
+                margin-top: 2rem;
+                margin-bottom: 1rem;
+                letter-spacing: 0.05em;
+              }
+              .prose p {
+                margin-bottom: 1.5rem;
+              }
+              .prose ul,
+              .prose ol {
+                margin-bottom: 1.5rem;
+                margin-left: 1.5rem;
+              }
+              .prose li {
+                margin-bottom: 0.5rem;
+                margin-left: 1rem;
+              }
+              .prose ul li {
+                list-style-type: disc;
+              }
+              .prose ol li {
+                list-style-type: decimal;
+              }
+              .prose code {
+                background-color: var(--muted);
+                padding: 0.25rem 0.5rem;
+                border-radius: 0.25rem;
+                font-size: 0.875rem;
+                font-family: monospace;
+              }
+              .prose pre {
+                background-color: var(--muted);
+                padding: 1rem;
+                border-radius: 0.5rem;
+                margin-bottom: 1.5rem;
+                overflow-x: auto;
+                border: 1px solid var(--border);
+              }
+              .prose pre code {
+                background-color: transparent;
+                padding: 0;
+                border-radius: 0;
+              }
+              .prose a {
+                color: #876f90;
+                text-decoration: underline;
+                transition: color 0.3s;
+              }
+              .prose a:hover {
+                color: #a087a0;
+              }
+              .prose blockquote {
+                border-left: 4px solid #876f90;
+                padding-left: 1rem;
+                padding-top: 0.5rem;
+                padding-bottom: 0.5rem;
+                font-style: italic;
+                opacity: 0.75;
+                margin-bottom: 1.5rem;
+              }
+            `}</style>
+            <div dangerouslySetInnerHTML={{ __html: content }} />
+          </div>
+        </article>
+
+        <PageFooter href='/blogs' />
+      </div>
+    );
+  } catch (error) {
+    return (
+      <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+        <div className='text-center py-12'>
+          <p className='text-2xl tracking-wider mb-4'>Blog post not found</p>
+          <Link
+            href='/blogs'
+            className='text-[#876f90] hover:text-[#a087a0] transition-colors'
+          >
+            ← Back to blogs
+          </Link>
+        </div>
+      </div>
+    );
+  }
+}
```

### `app/(portfolio)/blogs/page.tsx`

```diff
@@ -0,0 +1,62 @@
+import Link from 'next/link';
+import PageHeader from '@/components/bookfolio/components/PageHeader';
+import PageFooter from '@/components/bookfolio/components/PageFooter';
+import { getAllBlogPosts } from '@/lib/blog';
+import { RoughNotation } from 'react-rough-notation';
+import { formatDate } from '@/utils/date';
+
+export const metadata = {
+  title: 'Blog - Manish Bisht',
+  description: 'Articles about frontend development, web performance, and software engineering.',
+};
+
+export default function BlogsPage() {
+  const blogs = getAllBlogPosts();
+
+  return (
+    <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+      <PageHeader title='Blog' icon='✍︎' iconColor='#876f90' />
+
+      <div className='flex flex-col gap-8'>
+        <p className='tracking-wider opacity-50 text-xl'>
+          Thoughts on frontend development, software engineering, and building scalable systems.
+        </p>
+
+        {blogs.length === 0 ? (
+          <div className='text-center py-12'>
+            <p className='text-muted-foreground text-lg'>
+              No blog posts yet. Coming soon!
+            </p>
+          </div>
+        ) : (
+          <div className='flex flex-col gap-8'>
+            {blogs.map((blog) => (
+              <Link
+                key={blog.slug}
+                href={`/blogs/${blog.slug}`}
+                className='group flex flex-col gap-3 p-6 rounded-lg border border-border hover:border-muted-foreground transition-colors'
+              >
+                <div className='flex flex-col gap-2'>
+                  <h2 className='text-2xl tracking-wider group-hover:text-[#876f90] transition-colors'>
+                    {blog.metadata.title}
+                  </h2>
+                  <p className='text-muted-foreground tracking-wider'>
+                    {blog.metadata.description}
+                  </p>
+                </div>
+
+                <div className='flex gap-4 text-sm tracking-wider opacity-60'>
+                  <span>{formatDate(blog.metadata.date)}</span>
+                  <span>·</span>
+                  <span>{blog.metadata.reading_time} min read</span>
+                </div>
+              </Link>
+            ))}
+          </div>
+        )}
+      </div>
+
+      <PageFooter href='/' />
+    </div>
+  );
+}
```

### `components/bookfolio/Summary.tsx`

```diff
@@ -119,6 +119,26 @@ const Summary = () => {
 
       <p className='text-center text-muted-foreground text-4xl'>𓆝 𓆟 𓆞 𓆝 𓆟</p>
 
+      <div className='flex flex-col gap-6 items-end'>
+        <div className='flex flex-col gap-2 text-end w-fit'>
+          <p className='font-medium text-2xl text-[#876f90] tracking-wider'>
+            Writing & Thoughts
+          </p>
+          <p className='text-muted-foreground tracking-wider max-w-sm'>
+            Exploring frontend development, architecture patterns, and building scalable systems.
+          </p>
+        </div>
+
+        <Link
+          href='/blogs'
+          className='text-end flex gap-4 items-center justify-end text-[#876f90] text-xl w-fit'
+        >
+          Read articles <span>⁀જ➣</span>
+        </Link>
+      </div>
+
+      <p className='text-center text-muted-foreground text-4xl'>𓆝 𓆟 𓆞 𓆝 𓆟</p>
+
       <Quote quote="It's neither journey nor destination, it's who you become on that journey! ♡" />
 
       <PageFooter href='/' />
```

### `lib/blog.ts`

```diff
@@ -0,0 +1,66 @@
+import fs from 'fs';
+import path from 'path';
+import matter from 'gray-matter';
+import { marked } from 'marked';
+
+export interface BlogMetadata {
+  title: string;
+  description: string;
+  date: string;
+  author: string;
+  reading_time: number;
+  slug: string;
+}
+
+export interface BlogPost {
+  metadata: BlogMetadata;
+  content: string;
+}
+
+const blogsDirectory = path.join(process.cwd(), 'public/blogs');
+
+export function getBlogSlugs(): string[] {
+  if (!fs.existsSync(blogsDirectory)) return [];
+
+  return fs
+    .readdirSync(blogsDirectory)
+    .filter((file) => file.endsWith('.md'))
+    .map((file) => file.replace(/\.md$/, ''));
+}
+
+export function getBlogPost(slug: string): BlogPost {
+  const filePath = path.join(blogsDirectory, `${slug}.md`);
+  const fileContent = fs.readFileSync(filePath, 'utf8');
+  const { data, content } = matter(fileContent);
+
+  const metadata: BlogMetadata = {
+    title: data.title || '',
+    description: data.description || '',
+    date: data.date || '',
+    author: data.author || '',
+    reading_time: data.reading_time || 5,
+    slug,
+  };
+
+  return {
+    metadata,
+    content,
+  };
+}
+
+export function getAllBlogPosts(): (BlogPost & { slug: string })[] {
+  const slugs = getBlogSlugs();
+  return slugs
+    .map((slug) => {
+      const post = getBlogPost(slug);
+      return {
+        ...post,
+        slug,
+      };
+    })
+    .sort((a, b) => new Date(b.metadata.date).getTime() - new Date(a.metadata.date).getTime());
+}
+
+export async function renderMarkdown(markdown: string): Promise<string> {
+  return marked(markdown);
+}
```

### `package.json`

```diff
@@ -16,7 +16,9 @@
     "clsx": "^2.1.1",
     "date-fns": "^4.1.0",
     "geist": "^1.7.0",
+    "gray-matter": "^4.0.3",
     "lucide-react": "^1.8.0",
+    "marked": "^18.0.10",
     "motion": "^12.39.0",
     "next": "16.1.7",
     "radix-ui": "^1.4.3",
```

### `pnpm-lock.yaml`

```diff
@@ -20,9 +20,15 @@ importers:
       geist:
         specifier: ^1.7.0
         version: 1.7.0(next@16.1.7(@babel/core@7.29.0)(react-dom@19.2.5(react@19.2.5))(react@19.2.5))
+      gray-matter:
+        specifier: ^4.0.3
+        version: 4.0.3
       lucide-react:
         specifier: ^1.8.0
         version: 1.8.0(react@19.2.5)
+      marked:
+        specifier: ^18.0.10
+        version: 18.0.10
       motion:
         specifier: ^12.39.0
         version: 12.39.0(react-dom@19.2.5(react@19.2.5))(react@19.2.5)
@@ -1637,6 +1643,9 @@ packages:
     resolution: {integrity: sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==}
     engines: {node: '>=8'}
 
+  argparse@1.0.10:
+    resolution: {integrity: sha512-o5Roy6tNG4SL/FOkCAN6RzjiakZS25RLYFrcMttJqbdd8BWrnA+fGz57iN5Pb06pvBGvl5gQ0B48dJlslXvoTg==}
+
   argparse@2.0.1:
     resolution: {integrity: sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==}
 
@@ -2198,6 +2207,10 @@ packages:
     resolution: {integrity: sha512-hIS4idWWai69NezIdRt2xFVofaF4j+6INOpJlVOLDO8zXGpUVEVzIYk12UUi2JzjEzWL3IOAxcTubgz9Po0yXw==}
     engines: {node: '>= 18'}
 
+  extend-shallow@2.0.1:
+    resolution: {integrity: sha512-zCnTtlxNoAiDc3gqY2aYAWFx7XWWiasuF2K8Me5WbN8otHKTUKBwjPtNpRs/rbUZm7KxWAaNj7P1a/p52GbVug==}
+    engines: {node: '>=0.10.0'}
+
   fast-deep-equal@3.1.3:
     resolution: {integrity: sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==}
 
@@ -2391,6 +2404,10 @@ packages:
     resolution: {integrity: sha512-5bJ+nf/UCpAjHM8i06fl7eLyVC9iuNAjm9qzkiu2ZGhM0VscSvS6WDPfAwkdkBuoXGM9FJSbKl6wylMwP9Ktig==}
     engines: {node: ^12.22.0 || ^14.16.0 || ^16.0.0 || >=17.0.0}
 
+  gray-matter@4.0.3:
+    resolution: {integrity: sha512-5v6yZd4JK3eMI3FqqCouswVqwugaA9r4dNZB1wwcmrD02QkV5H0y7XBQW8QwQqEaZY1pM9aqORSORhJRdNK44Q==}
+    engines: {node: '>=6.0'}
+
   has-bigints@1.1.0:
     resolution: {integrity: sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==}
     engines: {node: '>= 0.4'}
@@ -2525,6 +2542,10 @@ packages:
     engines: {node: ^12.20.0 || ^14.13.1 || >=16.0.0}
     hasBin: true
 
+  is-extendable@0.1.1:
+    resolution: {integrity: sha512-5BMULNob1vgFX6EjQw5izWDxrecWK9AM72rugNr0TFldMOi0fj6Jk+zeKIt0xGj4cEfQIJth4w3OKWOJ4f+AFw==}
+    engines: {node: '>=0.10.0'}
+
   is-extglob@2.1.1:
     resolution: {integrity: sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==}
     engines: {node: '>=0.10.0'}
@@ -2672,6 +2693,10 @@ packages:
   js-tokens@4.0.0:
     resolution: {integrity: sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==}
 
+  js-yaml@3.15.1:
+    resolution: {integrity: sha512-S99WuO3HlhO3XN41EtYUNl9zzXjoJx7QvmipxsJVxtCBT0YHEFy+iOJhjSvrmV12nYhWpZaM8lPHkJm0yUMbag==}
+    hasBin: true
+
   js-yaml@4.1.1:
     resolution: {integrity: sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==}
     hasBin: true
@@ -2718,6 +2743,10 @@ packages:
   keyv@4.5.4:
     resolution: {integrity: sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==}
 
+  kind-of@6.0.3:
+    resolution: {integrity: sha512-dcS1ul+9tmeD95T+x28/ehLgd9mENa3LsvDTtzm3vyBEO7RPptvAD+t44WVXaUjTBRcrpFeFlC8WCruUR456hw==}
+    engines: {node: '>=0.10.0'}
+
   kleur@3.0.3:
     resolution: {integrity: sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w==}
     engines: {node: '>=6'}
@@ -2836,6 +2865,11 @@ packages:
   magic-string@0.30.21:
     resolution: {integrity: sha512-vd2F4YUyEXKGcLHoq+TEyCjxueSeHnFxyyjNp80yg0XV4vUhnDer/lvvlqM/arB5bXQN5K2/3oinyCRyx8T2CQ==}
 
+  marked@18.0.10:
+    resolution: {integrity: sha512-FJeH4bRpYoXiggcgriCGItKCSv3xkngJc4QCZ/rkQCogU3VYaLxYJoZl8Nw/b4+x7iij/pd+09mZ6A1dXzpL0A==}
+    engines: {node: '>= 20'}
+    hasBin: true
+
   math-intrinsics@1.1.0:
     resolution: {integrity: sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==}
     engines: {node: '>= 0.4'}
@@ -3371,6 +3405,10 @@ packages:
   scheduler@0.27.0:
     resolution: {integrity: sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q==}
 
+  section-matter@1.0.0:
+    resolution: {integrity: sha512-vfD3pmTzGpufjScBh50YHKzEu2lxBWhVEHsNGoEXmCmn2hKGfeNLYMzCJpe8cD7gqX7TJluOVpBkAequ6dgMmA==}
+    engines: {node: '>=4'}
+
   semver@6.3.1:
     resolution: {integrity: sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==}
     hasBin: true
@@ -3453,6 +3491,9 @@ packages:
     resolution: {integrity: sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==}
     engines: {node: '>=0.10.0'}
 
+  sprintf-js@1.0.3:
+    resolution: {integrity: sha512-D9cPgkvLlV3t3IzL0D0YLvGA9Ahk4PcvVwUbN0dSGr1aP0Nrt4AEnTUbuGvquEC0mA64Gqt1fzirlRs5ibXx8g==}
+
   stable-hash@0.0.5:
     resolution: {integrity: sha512-+L3ccpzibovGXFK+Ap/f8LOS0ahMrHTf3xu7mMLSpEGU0EO9ucaysSylKo9eRDFNhWve/y275iPmIZ4z39a9iA==}
 
@@ -3514,6 +3555,10 @@ packages:
     resolution: {integrity: sha512-yDPMNjp4WyfYBkHnjIRLfca1i6KMyGCtsVgoKe/z1+6vukgaENdgGBZt+ZmKPc4gavvEZ5OgHfHdrazhgNyG7w==}
     engines: {node: '>=12'}
 
+  strip-bom-string@1.0.0:
+    resolution: {integrity: sha512-uCC2VHvQRYu+lMh4My/sFNmF2klFymLX1wHJeXnbEJERpV/ZsVuonzerjfrGpIGF7LBVa1O7i9kjiWvJiFck8g==}
+    engines: {node: '>=0.10.0'}
+
   strip-bom@3.0.0:
     resolution: {integrity: sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==}
     engines: {node: '>=4'}
@@ -5412,6 +5457,10 @@ snapshots:
     dependencies:
       color-convert: 2.0.1
 
+  argparse@1.0.10:
+    dependencies:
+      sprintf-js: 1.0.3
+
   argparse@2.0.1: {}
 
   aria-hidden@1.2.6:
@@ -6146,6 +6195,10 @@ snapshots:
     transitivePeerDependencies:
       - supports-color
 
+  extend-shallow@2.0.1:
+    dependencies:
+      is-extendable: 0.1.1
+
   fast-deep-equal@3.1.3: {}
 
   fast-glob@3.3.1:
@@ -6334,6 +6387,13 @@ snapshots:
 
   graphql@16.13.2: {}
 
+  gray-matter@4.0.3:
+    dependencies:
+      js-yaml: 3.15.1
+      kind-of: 6.0.3
+      section-matter: 1.0.0
+      strip-bom-string: 1.0.0
+
   has-bigints@1.1.0: {}
 
   has-flag@4.0.0: {}
@@ -6460,6 +6520,8 @@ snapshots:
 
   is-docker@3.0.0: {}
 
+  is-extendable@0.1.1: {}
+
   is-extglob@2.1.1: {}
 
   is-finalizationregistry@1.1.1:
@@ -6581,6 +6643,11 @@ snapshots:
 
   js-tokens@4.0.0: {}
 
+  js-yaml@3.15.1:
+    dependencies:
+      argparse: 1.0.10
+      esprima: 4.0.1
+
   js-yaml@4.1.1:
     dependencies:
       argparse: 2.0.1
@@ -6622,6 +6689,8 @@ snapshots:
     dependencies:
       json-buffer: 3.0.1
 
+  kind-of@6.0.3: {}
+
   kleur@3.0.3: {}
 
   kleur@4.1.5: {}
@@ -6715,6 +6784,8 @@ snapshots:
     dependencies:
       '@jridgewell/sourcemap-codec': 1.5.5
 
+  marked@18.0.10: {}
+
   math-intrinsics@1.1.0: {}
 
   media-typer@1.1.0: {}
@@ -7260,6 +7331,11 @@ snapshots:
 
   scheduler@0.27.0: {}
 
+  section-matter@1.0.0:
+    dependencies:
+      extend-shallow: 2.0.1
+      kind-of: 6.0.3
+
   semver@6.3.1: {}
 
   semver@7.7.4: {}
@@ -7432,6 +7508,8 @@ snapshots:
 
   source-map@0.6.1: {}
 
+  sprintf-js@1.0.3: {}
+
   stable-hash@0.0.5: {}
 
   statuses@2.0.2: {}
@@ -7521,6 +7599,8 @@ snapshots:
     dependencies:
       ansi-regex: 6.2.2
 
+  strip-bom-string@1.0.0: {}
+
   strip-bom@3.0.0: {}
 
   strip-final-newline@2.0.0: {}
```

### `public/blogs/building-automated-blog-generation.md`

```diff
@@ -0,0 +1,57 @@
+# Building an Automated Daily Blog Generation System
+
+## Context
+
+I've been managing multiple side projects and wanted a way to automatically surface interesting technical work into blog posts. The challenge: manually reviewing commit history and writing about it is time-consuming and I often miss valuable stories worth sharing.
+
+## Problem
+
+Every day, I push code to various repositories, but most of that work isn't blog-worthy:
+- README updates
+- Dependency bumps
+- Typo fixes
+- Routine refactors
+
+The rare gems—difficult debugging sessions, architectural decisions, performance improvements, or lessons learned from failures—often go undocumented and forgotten.
+
+## Solution: Daily Blog Agent
+
+I built an automated pipeline that:
+
+1. **Collects commits** from all GitHub repositories authored by me on a given day
+2. **Fetches detailed diffs** for each commit
+3. **Runs Claude** to analyze whether the work contains a genuine technical story
+4. **Generates markdown drafts** only when the story is worth telling
+
+### The Architecture
+
+```
+daily.sh
+  ├─ collect_commits.py    [GitHub Search API]
+  ├─ collect_diffs.py      [GitHub REST API]
+  └─ claude (agent)        [Analyzes & writes]
+```
+
+### Key Insights
+
+**Using the GitHub Search API** was crucial for performance. Rather than iterating through every repository and checking for commits (O(n) repos), the search API queries directly for commits by author and date across all repos in one request.
+
+**Filtering at the source** saves token usage. Instead of fetching all diffs and asking Claude to filter, the agent receives only the raw data and makes intelligent decisions about what's worth a story.
+
+**Permission modes** in Claude Code eliminated interactive prompts. Setting `--permission-mode acceptEdits` in the shell script allows the agent to read input files and write drafts without requiring manual approval.
+
+### Technical Lessons
+
+1. **API efficiency matters** – Search API over repo enumeration
+2. **Let the AI decide** – Provide data, don't pre-judge what's interesting
+3. **Automate the routine** – Removes friction from the writing process
+4. **Version control the prompts** – The agent's instructions are configuration
+
+## What's Next
+
+The system generates draft files for manual review. Future iterations could:
+- Automatically commit drafts to the portfolio repository
+- Generate social media summaries
+- Track which stories actually get published and learn from patterns
+
+This approach turns passive commit history into a writing prompt machine.
```

### `public/blogs/building-scalable-frontends.md`

```diff
@@ -0,0 +1,124 @@
+---
+title: Building Scalable Frontend Systems
+description: A deep dive into architectural patterns and best practices for building frontend systems that scale.
+date: 2026-08-15
+author: Manish Bisht
+reading_time: 8
+---
+
+# Building Scalable Frontend Systems
+
+When you start a new frontend project, everything feels simple. A few components here, some state management there, and you're done. But as your application grows, complexity compounds. Features pile up, components become interdependent, and suddenly adding a single button feels like moving a mountain.
+
+The question isn't whether your frontend will need to scale—it's whether you'll be ready when it does.
+
+## The Architecture Problem
+
+I've seen many teams approach scaling reactively. They write code that works, ship features, and when performance or maintainability becomes an issue, they scramble to refactor. This is expensive, error-prone, and demoralizing.
+
+The better approach? Think about scalability from day one.
+
+### Component Organization
+
+Your first instinct might be to organize by file type:
+
+```
+components/
+  buttons/
+  inputs/
+  modals/
+  ...
+```
+
+This approach works for small projects but becomes a nightmare at scale. When you need to change a component, you're hunting across multiple directories.
+
+Instead, organize by feature:
+
+```
+components/
+  auth/
+    LoginForm.tsx
+    RegisterForm.tsx
+    PasswordReset.tsx
+  dashboard/
+    Dashboard.tsx
+    Charts.tsx
+    Widgets.tsx
+  shared/
+    Button.tsx
+    Input.tsx
+    Card.tsx
+```
+
+This structure makes it clear which components belong together and easier to maintain related functionality.
+
+## State Management Strategy
+
+The state management landscape is crowded. Redux, Zustand, Jotai, Recoil—each has merits. But the real question isn't which tool to use; it's *when* you need centralized state at all.
+
+**Local state first.** Keep state as close to where it's used as possible. `useState` for a form? Perfect. A modal's open state? Great.
+
+**Component communication through props.** If you have a few levels of nesting, prop drilling isn't that painful, and it makes data flow explicit.
+
+**Global state when necessary.** Only reach for a state management library when multiple unrelated parts of your app need the same data, or when performance requires it.
+
+## Performance Optimization
+
+Scalability isn't just about code organization—it's about how your app performs as it grows.
+
+### Code Splitting
+
+Load only what you need:
+
+```tsx
+import dynamic from 'next/dynamic';
+
+const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
+  loading: () => <Skeleton />,
+});
+```
+
+### Memoization (Use Carefully)
+
+Premature optimization is the root of all evil. Only memoize when you've measured and found a bottleneck.
+
+```tsx
+const ExpensiveComponent = memo(({ data }) => {
+  return <div>{/* render something expensive */}</div>;
+});
+```
+
+### Virtual Scrolling for Large Lists
+
+When you have hundreds of items, render only the visible ones:
+
+```tsx
+<VirtualList items={items} renderItem={renderRow} />
+```
+
+## Testing at Scale
+
+As your codebase grows, tests become your safety net. But testing everything is impossible.
+
+Focus your testing efforts:
+
+1. **Unit tests** for pure functions and utilities
+2. **Integration tests** for component interactions
+3. **E2E tests** for critical user flows
+
+Write the test that would have caught each bug you've shipped. Over time, you'll build confidence in your ability to refactor safely.
+
+## Monitoring and Observability
+
+You can't improve what you don't measure.
+
+- **Web Vitals:** Use tools like web-vitals to track Core Web Vitals
+- **Error tracking:** Integrate Sentry or similar to catch production errors
+- **Analytics:** Understand how users actually use your app
+- **Performance profiling:** Regularly profile your app to find bottlenecks
+
+## Conclusion
+
+Building scalable frontends isn't about being perfect from day one. It's about making deliberate choices that leave room for growth, making it easy to maintain as complexity increases, and measuring to know when to optimize.
+
+Start simple, think ahead, measure often, and refactor when needed. Your future self will thank you.
```

### `utils/date.ts`

```diff
@@ -1,4 +1,4 @@
-import { intervalToDuration } from 'date-fns';
+import { intervalToDuration, format } from 'date-fns';
 
 function parseMonthYear(input: string) {
   const [month, year] = input.split('/').map(Number);
@@ -16,3 +16,12 @@ export function getDuration(startDate: string, endDate?: string) {
   if (months) return `${months}m`;
   return '0m';
 }
+
+export function formatDate(dateString: string): string {
+  try {
+    const date = new Date(dateString);
+    return format(date, 'MMM d, yyyy');
+  } catch {
+    return dateString;
+  }
+}
```

---

## ManishBisht777/Kyogre

### Commit `95387d6b0b396748da2f592eca5e77b23a09510c`

**Message:** blog generation, implmenting blog to portfolio and pr raise to master

### `.claude/settings.json`

```diff
@@ -0,0 +1,6 @@
+{
+  "permissions": {
+    "read": ["allow"],
+    "write": ["allow"]
+  }
+}
```

### `src/kyogre/scripts/daily.py`

```diff
@@ -0,0 +1,194 @@
+#!/usr/bin/env python3
+
+import os
+import sys
+import subprocess
+from pathlib import Path
+
+SCRIPT_DIR = Path(__file__).parent
+AGENT_DIR = SCRIPT_DIR.parent
+PORTFOLIO_REPO = Path("/Users/manishbisht/Desktop/dev/manish/portfolio")
+BLOG_DIR = PORTFOLIO_REPO / "public" / "blogs"
+
+print("=" * 32)
+print(" Personal Blog Agent")
+print("=" * 32)
+
+print("\n1. Collecting commits...")
+subprocess.run(
+    ["uv", "run", "python", str(AGENT_DIR / "tools/collect_commits.py")],
+    cwd=AGENT_DIR,
+    check=True,
+)
+
+print("\n2. Collecting diffs...")
+subprocess.run(
+    ["uv", "run", "python", str(AGENT_DIR / "tools/collect_diffs.py")],
+    cwd=AGENT_DIR,
+    check=True,
+)
+
+print("\n3. Running Claude...")
+
+prompt = """
+You are my personal engineering blog agent.
+
+Read these files first:
+
+temp/commits.md
+temp/diffs.md
+
+Analyze today's GitHub activity.
+
+Determine whether there is a genuinely valuable
+technical story.
+
+Ignore:
+- typo fixes
+- README changes
+- dependency updates
+- variable renames
+- trivial refactors
+- simple UI changes
+
+Prefer:
+- difficult debugging
+- architectural decisions
+- interesting implementations
+- performance improvements
+- AI/LLM experiments
+- failures
+- tradeoffs
+- unexpected technical problems
+- useful engineering lessons
+
+If the work is NOT blog-worthy:
+
+Do not create anything inside drafts/.
+Simply report that there is no suitable blog.
+
+If the work IS blog-worthy:
+
+Create exactly one Markdown file inside:
+
+drafts/
+
+Use a descriptive slug, for example:
+
+drafts/building-a-reliable-ai-agent.md
+
+The article must be based ONLY on:
+- temp/commits.md
+- temp/diffs.md
+- the actual repository code when necessary
+
+Do not invent:
+- metrics
+- users
+- production usage
+- benchmarks
+- technologies
+- implementation details
+
+The article should explain:
+
+1. Context
+2. Problem
+3. What was tried
+4. What failed
+5. Final solution
+6. Technical reasoning
+7. Lessons learned
+
+After writing the article, review it for accuracy.
+
+Do NOT publish it.
+Do NOT modify the portfolio repository.
+Do NOT delete anything.
+"""
+
+result = subprocess.run(
+    ["claude", "--permission-mode", "acceptEdits", "-p", prompt],
+    cwd=AGENT_DIR,
+    check=True,
+)
+
+print("\n4. Checking generated drafts...")
+
+drafts_dir = AGENT_DIR / "drafts"
+draft_files = list(drafts_dir.glob("*.md")) if drafts_dir.exists() else []
+
+if not draft_files:
+    print("No blog was generated.")
+    (AGENT_DIR / "temp" / "commits.md").unlink(missing_ok=True)
+    (AGENT_DIR / "temp" / "diffs.md").unlink(missing_ok=True)
+    sys.exit(0)
+
+if len(draft_files) > 1:
+    print("ERROR: Claude generated more than one draft.")
+    print("Keeping everything for manual inspection.")
+    sys.exit(1)
+
+draft = draft_files[0]
+draft_filename = draft.name
+print(f"Draft found: {draft_filename}")
+
+print("\n5. Checking portfolio repository...")
+os.chdir(PORTFOLIO_REPO)
+
+result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
+if result.stdout.strip():
+    print("ERROR: Portfolio repository has uncommitted changes.")
+    print(result.stdout)
+    sys.exit(1)
+
+print("\n6. Copying blog...")
+blog_dest = BLOG_DIR / draft_filename
+import shutil
+shutil.copy(draft, blog_dest)
+
+print("\n7. Creating branch...")
+branch_name = f"blog/{draft_filename[:-3]}"
+subprocess.run(["git", "checkout", "-b", branch_name], check=True)
+
+print("\n8. Checking changes...")
+result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
+changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
+if len(changed_files) != 1:
+    print("ERROR: Unexpected files changed.")
+    print(result.stdout)
+    sys.exit(1)
+
+print("\n9. Committing...")
+subprocess.run(["git", "add", str(blog_dest)], check=True)
+subprocess.run(
+    ["git", "commit", "-m", f"docs: add {draft_filename[:-3]}"],
+    check=True,
+)
+
+print("\n10. Pushing...")
+subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
+
+print("\n11. Creating PR to master...")
+subprocess.run(
+    ["gh", "pr", "create",
+     "--base", "master",
+     "--head", branch_name,
+     "--title", f"docs: add {draft_filename[:-3]}",
+     "--body", "Auto-generated blog post from today's commits."],
+    check=True,
+)
+
+print("\n12. Publishing succeeded.")
+os.chdir(AGENT_DIR)
+
+draft.unlink()
+(AGENT_DIR / "temp" / "commits.md").unlink(missing_ok=True)
+(AGENT_DIR / "temp" / "diffs.md").unlink(missing_ok=True)
+
+print("\n" + "=" * 32)
+print(" SUCCESS")
+print("=" * 32)
+print(f"Blog: {draft_filename}")
+print(f"Branch: {branch_name}")
+print("Draft removed.")
```

### `src/kyogre/scripts/daily.sh`

```diff
@@ -0,0 +1,182 @@
+#!/bin/bash
+
+set -euo pipefail
+
+AGENT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
+PORTFOLIO_REPO="/Users/manishbisht/Desktop/dev/manish/portfolio"
+BLOG_DIR="$PORTFOLIO_REPO/public/blogs"
+cd "$AGENT_DIR"
+
+echo "================================"
+echo " Personal Blog Agent"
+echo "================================"
+
+echo ""
+echo "1. Collecting commits..."
+
+uv run python tools/collect_commits.py
+
+echo ""
+echo "2. Collecting diffs..."
+
+uv run python tools/collect_diffs.py
+
+echo ""
+echo "3. Running Claude..."
+
+claude --permission-mode acceptEdits -p "
+You are my personal engineering blog agent.
+
+Read:
+
+temp/commits.md
+temp/diffs.md
+
+Analyze today's GitHub activity.
+
+Determine whether there is a genuinely valuable
+technical story.
+
+Ignore trivial changes.
+
+Prefer:
+- difficult debugging
+- architectural decisions
+- interesting implementations
+- performance improvements
+- AI/LLM experiments
+- failures
+- tradeoffs
+- useful engineering lessons
+
+If the work is NOT blog-worthy:
+
+Do not create a draft.
+
+If the work IS blog-worthy:
+
+Create exactly one Markdown file inside:
+
+drafts/
+
+The article should contain:
+
+1. Context
+2. Problem
+3. What was tried
+4. What failed
+5. Final solution
+6. Technical reasoning
+7. Lessons learned
+
+Use only information supported by the GitHub
+activity and repository.
+
+Do not invent metrics, users, production usage,
+benchmarks, technologies, or implementation details.
+
+Review the article for technical accuracy.
+
+Do NOT publish anything.
+Do NOT modify the portfolio repository.
+"
+
+echo ""
+echo "4. Checking drafts..."
+
+DRAFT_COUNT=$(find drafts -maxdepth 1 -type f -name "*.md" | wc -l | tr -d ' ')
+
+if [ "$DRAFT_COUNT" -eq 0 ]; then
+    echo "No blog-worthy work today."
+
+    rm -f temp/commits.md
+    rm -f temp/diffs.md
+
+    exit 0
+fi
+
+if [ "$DRAFT_COUNT" -gt 1 ]; then
+    echo "ERROR: More than one draft generated."
+    exit 1
+fi
+
+DRAFT=$(find drafts -maxdepth 1 -type f -name "*.md" | head -n 1)
+
+BLOG_FILENAME=$(basename "$DRAFT")
+
+echo ""
+echo "Draft:"
+echo "$BLOG_FILENAME"
+
+echo ""
+echo "5. Checking portfolio repository..."
+
+cd "$PORTFOLIO_REPO"
+
+if [ -n "$(git status --porcelain)" ]; then
+    echo "ERROR: Portfolio repository has uncommitted changes."
+    git status --short
+    exit 1
+fi
+
+echo ""
+echo "6. Copying blog..."
+
+cp "$AGENT_DIR/$DRAFT" "$BLOG_DIR/$BLOG_FILENAME"
+
+echo ""
+echo "7. Creating branch..."
+
+BRANCH_NAME="blog/${BLOG_FILENAME%.md}"
+
+git checkout -b "$BRANCH_NAME"
+
+echo ""
+echo "8. Checking changes..."
+
+CHANGED_FILE_COUNT=$(git status --short | wc -l | tr -d ' ')
+
+if [ "$CHANGED_FILE_COUNT" -ne 1 ]; then
+    echo "ERROR: Unexpected files changed."
+    git status --short
+    exit 1
+fi
+
+echo ""
+echo "9. Committing..."
+
+git add "$BLOG_DIR/$BLOG_FILENAME"
+
+git commit \
+    -m "docs: add ${BLOG_FILENAME%.md}"
+
+echo ""
+echo "10. Pushing..."
+
+git push -u origin "$BRANCH_NAME"
+
+echo ""
+echo "11. Creating PR to master..."
+
+gh pr create \
+    --base master \
+    --head "$BRANCH_NAME" \
+    --title "docs: add ${BLOG_FILENAME%.md}" \
+    --body "Auto-generated blog post from today's commits."
+
+echo ""
+echo "12. Publishing succeeded."
+
+cd "$AGENT_DIR"
+
+rm "$DRAFT"
+rm -f temp/commits.md
+rm -f temp/diffs.md
+
+echo ""
+echo "================================"
+echo " SUCCESS"
+echo "================================"
+echo "Blog: $BLOG_FILENAME"
+echo "Branch: $BRANCH_NAME"
+echo "Draft removed."
\ No newline at end of file
```

### `src/kyogre/tools/collect_commits.py`

```diff
Patch unavailable
```

### `src/kyogre/tools/collect_diffs.py`

```diff
@@ -0,0 +1,91 @@
+import os
+
+import requests
+from dotenv import load_dotenv
+
+
+load_dotenv()
+
+GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
+GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
+
+HEADERS = {
+    "Authorization": f"Bearer {GITHUB_TOKEN}",
+    "Accept": "application/vnd.github+json",
+}
+
+
+def get_commit(repo_full_name, sha):
+    response = requests.get(
+        f"https://api.github.com/repos/{repo_full_name}/commits/{sha}",
+        headers=HEADERS,
+    )
+
+    response.raise_for_status()
+
+    return response.json()
+
+
+def main():
+    with open("temp/commits.md") as file:
+        content = file.read()
+
+    lines = content.splitlines()
+
+    commits = []
+
+    current_repo = None
+    current_sha = None
+
+    for line in lines:
+        if line.startswith("## "):
+            current_repo = line[3:].strip()
+
+        if line.startswith("**SHA:**"):
+            current_sha = (
+                line.split("`")[1]
+            )
+
+            commits.append({
+                "repo": current_repo,
+                "sha": current_sha,
+            })
+
+    with open("temp/diffs.md", "w") as file:
+        file.write("# GitHub Diffs\n\n")
+
+        for commit in commits:
+            data = get_commit(
+                commit["repo"],
+                commit["sha"],
+            )
+
+            file.write(
+                f"## {commit['repo']}\n\n"
+                f"### Commit `{commit['sha']}`\n\n"
+            )
+
+            file.write(
+                f"**Message:** "
+                f"{data['commit']['message']}\n\n"
+            )
+
+            for changed_file in data.get("files", []):
+                filename = changed_file["filename"]
+                patch = changed_file.get(
+                    "patch",
+                    "Patch unavailable",
+                )
+
+                file.write(
+                    f"### `{filename}`\n\n"
+                    f"```diff\n"
+                    f"{patch}\n"
+                    f"```\n\n"
+                )
+
+            file.write("---\n\n")
+
+
+if __name__ == "__main__":
+    main()
\ No newline at end of file
```

### `temp/diffs.md`

```diff
@@ -0,0 +1,32 @@
+# GitHub Diffs
+
+## ManishBisht777/Arceus
+
+### Commit `2b87aa6deeb516cb64108189d1fe4b156ccf331c`
+
+**Message:** Update README by removing license section
+
+Removed license section and cleaned up author information.
+
+### `README.md`
+
+```diff
+@@ -407,13 +407,9 @@ To extend or modify Arceus:
+ - Check GH_TOKEN is valid and has repo permissions
+ - Ensure ARCEUS_PROD_BRANCH exists on remote
+ 
+-## 📄 License
+-
+-[Specify your project's license]
+-
+ ## 👤 Author
+ 
+-Manish Bisht (manish@delightree.com)
++Manish Bisht
+ 
+ ---
+ 
+```
+
+---
+
```

---

## ManishBisht777/portfolio

### Commit `ba6b4c3264cba1946ab738353043b86df2cc34e0`

**Message:** docs: add building-automated-blog-generation

### `public/blogs/building-automated-blog-generation.md`

```diff
@@ -0,0 +1,57 @@
+# Building an Automated Daily Blog Generation System
+
+## Context
+
+I've been managing multiple side projects and wanted a way to automatically surface interesting technical work into blog posts. The challenge: manually reviewing commit history and writing about it is time-consuming and I often miss valuable stories worth sharing.
+
+## Problem
+
+Every day, I push code to various repositories, but most of that work isn't blog-worthy:
+- README updates
+- Dependency bumps
+- Typo fixes
+- Routine refactors
+
+The rare gems—difficult debugging sessions, architectural decisions, performance improvements, or lessons learned from failures—often go undocumented and forgotten.
+
+## Solution: Daily Blog Agent
+
+I built an automated pipeline that:
+
+1. **Collects commits** from all GitHub repositories authored by me on a given day
+2. **Fetches detailed diffs** for each commit
+3. **Runs Claude** to analyze whether the work contains a genuine technical story
+4. **Generates markdown drafts** only when the story is worth telling
+
+### The Architecture
+
+```
+daily.sh
+  ├─ collect_commits.py    [GitHub Search API]
+  ├─ collect_diffs.py      [GitHub REST API]
+  └─ claude (agent)        [Analyzes & writes]
+```
+
+### Key Insights
+
+**Using the GitHub Search API** was crucial for performance. Rather than iterating through every repository and checking for commits (O(n) repos), the search API queries directly for commits by author and date across all repos in one request.
+
+**Filtering at the source** saves token usage. Instead of fetching all diffs and asking Claude to filter, the agent receives only the raw data and makes intelligent decisions about what's worth a story.
+
+**Permission modes** in Claude Code eliminated interactive prompts. Setting `--permission-mode acceptEdits` in the shell script allows the agent to read input files and write drafts without requiring manual approval.
+
+### Technical Lessons
+
+1. **API efficiency matters** – Search API over repo enumeration
+2. **Let the AI decide** – Provide data, don't pre-judge what's interesting
+3. **Automate the routine** – Removes friction from the writing process
+4. **Version control the prompts** – The agent's instructions are configuration
+
+## What's Next
+
+The system generates draft files for manual review. Future iterations could:
+- Automatically commit drafts to the portfolio repository
+- Generate social media summaries
+- Track which stories actually get published and learn from patterns
+
+This approach turns passive commit history into a writing prompt machine.
```

---

## ManishBisht777/portfolio

### Commit `7cfd1787a2cf5615cd370d31e7554c64f5b24363`

**Message:** Add blog feature with blog listing and individual blog post pages

- Create blog listing page at /blogs showing all blog posts with titles, descriptions, and reading times
- Add dynamic blog post page that renders markdown content with proper styling
- Create utility functions for parsing markdown files with gray-matter and rendering with marked
- Add sample blog post "Building Scalable Frontend Systems" covering architecture patterns
- Update home page with link to blog section
- Add gray-matter and marked dependencies for markdown parsing

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>

### `app/(portfolio)/blogs/[slug]/page.tsx`

```diff
@@ -0,0 +1,162 @@
+import Link from 'next/link';
+import PageFooter from '@/components/bookfolio/components/PageFooter';
+import { getBlogPost, getBlogSlugs, renderMarkdown } from '@/lib/blog';
+import { formatDate } from '@/utils/date';
+
+interface Props {
+  params: Promise<{ slug: string }>;
+}
+
+export async function generateStaticParams() {
+  const slugs = getBlogSlugs();
+  return slugs.map((slug) => ({ slug }));
+}
+
+export async function generateMetadata({ params }: Props) {
+  const { slug } = await params;
+  try {
+    const post = getBlogPost(slug);
+    return {
+      title: `${post.metadata.title} - Manish Bisht`,
+      description: post.metadata.description,
+    };
+  } catch {
+    return { title: 'Blog - Manish Bisht' };
+  }
+}
+
+export default async function BlogPostPage({ params }: Props) {
+  const { slug } = await params;
+
+  try {
+    const post = getBlogPost(slug);
+    const content = await renderMarkdown(post.content);
+
+    return (
+      <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+        <div>
+          <Link
+            href='/blogs'
+            className='text-[#876f90] hover:text-[#a087a0] transition-colors flex items-center gap-2 w-fit tracking-wider text-lg'
+          >
+            <span>←</span> Back to blogs
+          </Link>
+        </div>
+
+        <article className='flex flex-col gap-8'>
+          <div className='flex flex-col gap-4'>
+            <h1 className='text-5xl tracking-wider leading-tight md:text-6xl'>
+              {post.metadata.title}
+            </h1>
+            <div className='flex gap-4 text-muted-foreground tracking-wider text-lg flex-wrap'>
+              <span>{post.metadata.author || 'Manish Bisht'}</span>
+              <span>·</span>
+              <span>{formatDate(post.metadata.date)}</span>
+              <span>·</span>
+              <span>{post.metadata.reading_time || 5} min read</span>
+            </div>
+          </div>
+
+          <div
+            className='prose prose-invert max-w-none tracking-wider leading-relaxed'
+            style={{
+              '--tw-prose-body': 'var(--foreground)',
+              '--tw-prose-headings': 'var(--foreground)',
+              '--tw-prose-links': '#876f90',
+              '--tw-prose-code': 'var(--foreground)',
+            } as React.CSSProperties}
+          >
+            <style>{`
+              .prose h2 {
+                font-size: 1.875rem;
+                font-weight: 600;
+                margin-top: 3rem;
+                margin-bottom: 1.5rem;
+                letter-spacing: 0.05em;
+              }
+              .prose h3 {
+                font-size: 1.5rem;
+                font-weight: 500;
+                margin-top: 2rem;
+                margin-bottom: 1rem;
+                letter-spacing: 0.05em;
+              }
+              .prose p {
+                margin-bottom: 1.5rem;
+              }
+              .prose ul,
+              .prose ol {
+                margin-bottom: 1.5rem;
+                margin-left: 1.5rem;
+              }
+              .prose li {
+                margin-bottom: 0.5rem;
+                margin-left: 1rem;
+              }
+              .prose ul li {
+                list-style-type: disc;
+              }
+              .prose ol li {
+                list-style-type: decimal;
+              }
+              .prose code {
+                background-color: var(--muted);
+                padding: 0.25rem 0.5rem;
+                border-radius: 0.25rem;
+                font-size: 0.875rem;
+                font-family: monospace;
+              }
+              .prose pre {
+                background-color: var(--muted);
+                padding: 1rem;
+                border-radius: 0.5rem;
+                margin-bottom: 1.5rem;
+                overflow-x: auto;
+                border: 1px solid var(--border);
+              }
+              .prose pre code {
+                background-color: transparent;
+                padding: 0;
+                border-radius: 0;
+              }
+              .prose a {
+                color: #876f90;
+                text-decoration: underline;
+                transition: color 0.3s;
+              }
+              .prose a:hover {
+                color: #a087a0;
+              }
+              .prose blockquote {
+                border-left: 4px solid #876f90;
+                padding-left: 1rem;
+                padding-top: 0.5rem;
+                padding-bottom: 0.5rem;
+                font-style: italic;
+                opacity: 0.75;
+                margin-bottom: 1.5rem;
+              }
+            `}</style>
+            <div dangerouslySetInnerHTML={{ __html: content }} />
+          </div>
+        </article>
+
+        <PageFooter href='/blogs' />
+      </div>
+    );
+  } catch (error) {
+    return (
+      <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+        <div className='text-center py-12'>
+          <p className='text-2xl tracking-wider mb-4'>Blog post not found</p>
+          <Link
+            href='/blogs'
+            className='text-[#876f90] hover:text-[#a087a0] transition-colors'
+          >
+            ← Back to blogs
+          </Link>
+        </div>
+      </div>
+    );
+  }
+}
```

### `app/(portfolio)/blogs/page.tsx`

```diff
@@ -0,0 +1,62 @@
+import Link from 'next/link';
+import PageHeader from '@/components/bookfolio/components/PageHeader';
+import PageFooter from '@/components/bookfolio/components/PageFooter';
+import { getAllBlogPosts } from '@/lib/blog';
+import { RoughNotation } from 'react-rough-notation';
+import { formatDate } from '@/utils/date';
+
+export const metadata = {
+  title: 'Blog - Manish Bisht',
+  description: 'Articles about frontend development, web performance, and software engineering.',
+};
+
+export default function BlogsPage() {
+  const blogs = getAllBlogPosts();
+
+  return (
+    <div className='flex justify-center flex-col gap-12 px-10 py-12 md:gap-20 md:px-2 md:py-20'>
+      <PageHeader title='Blog' icon='✍︎' iconColor='#876f90' />
+
+      <div className='flex flex-col gap-8'>
+        <p className='tracking-wider opacity-50 text-xl'>
+          Thoughts on frontend development, software engineering, and building scalable systems.
+        </p>
+
+        {blogs.length === 0 ? (
+          <div className='text-center py-12'>
+            <p className='text-muted-foreground text-lg'>
+              No blog posts yet. Coming soon!
+            </p>
+          </div>
+        ) : (
+          <div className='flex flex-col gap-8'>
+            {blogs.map((blog) => (
+              <Link
+                key={blog.slug}
+                href={`/blogs/${blog.slug}`}
+                className='group flex flex-col gap-3 p-6 rounded-lg border border-border hover:border-muted-foreground transition-colors'
+              >
+                <div className='flex flex-col gap-2'>
+                  <h2 className='text-2xl tracking-wider group-hover:text-[#876f90] transition-colors'>
+                    {blog.metadata.title}
+                  </h2>
+                  <p className='text-muted-foreground tracking-wider'>
+                    {blog.metadata.description}
+                  </p>
+                </div>
+
+                <div className='flex gap-4 text-sm tracking-wider opacity-60'>
+                  <span>{formatDate(blog.metadata.date)}</span>
+                  <span>·</span>
+                  <span>{blog.metadata.reading_time} min read</span>
+                </div>
+              </Link>
+            ))}
+          </div>
+        )}
+      </div>
+
+      <PageFooter href='/' />
+    </div>
+  );
+}
```

### `components/bookfolio/Summary.tsx`

```diff
@@ -119,6 +119,26 @@ const Summary = () => {
 
       <p className='text-center text-muted-foreground text-4xl'>𓆝 𓆟 𓆞 𓆝 𓆟</p>
 
+      <div className='flex flex-col gap-6 items-end'>
+        <div className='flex flex-col gap-2 text-end w-fit'>
+          <p className='font-medium text-2xl text-[#876f90] tracking-wider'>
+            Writing & Thoughts
+          </p>
+          <p className='text-muted-foreground tracking-wider max-w-sm'>
+            Exploring frontend development, architecture patterns, and building scalable systems.
+          </p>
+        </div>
+
+        <Link
+          href='/blogs'
+          className='text-end flex gap-4 items-center justify-end text-[#876f90] text-xl w-fit'
+        >
+          Read articles <span>⁀જ➣</span>
+        </Link>
+      </div>
+
+      <p className='text-center text-muted-foreground text-4xl'>𓆝 𓆟 𓆞 𓆝 𓆟</p>
+
       <Quote quote="It's neither journey nor destination, it's who you become on that journey! ♡" />
 
       <PageFooter href='/' />
```

### `lib/blog.ts`

```diff
@@ -0,0 +1,66 @@
+import fs from 'fs';
+import path from 'path';
+import matter from 'gray-matter';
+import { marked } from 'marked';
+
+export interface BlogMetadata {
+  title: string;
+  description: string;
+  date: string;
+  author: string;
+  reading_time: number;
+  slug: string;
+}
+
+export interface BlogPost {
+  metadata: BlogMetadata;
+  content: string;
+}
+
+const blogsDirectory = path.join(process.cwd(), 'public/blogs');
+
+export function getBlogSlugs(): string[] {
+  if (!fs.existsSync(blogsDirectory)) return [];
+
+  return fs
+    .readdirSync(blogsDirectory)
+    .filter((file) => file.endsWith('.md'))
+    .map((file) => file.replace(/\.md$/, ''));
+}
+
+export function getBlogPost(slug: string): BlogPost {
+  const filePath = path.join(blogsDirectory, `${slug}.md`);
+  const fileContent = fs.readFileSync(filePath, 'utf8');
+  const { data, content } = matter(fileContent);
+
+  const metadata: BlogMetadata = {
+    title: data.title || '',
+    description: data.description || '',
+    date: data.date || '',
+    author: data.author || '',
+    reading_time: data.reading_time || 5,
+    slug,
+  };
+
+  return {
+    metadata,
+    content,
+  };
+}
+
+export function getAllBlogPosts(): (BlogPost & { slug: string })[] {
+  const slugs = getBlogSlugs();
+  return slugs
+    .map((slug) => {
+      const post = getBlogPost(slug);
+      return {
+        ...post,
+        slug,
+      };
+    })
+    .sort((a, b) => new Date(b.metadata.date).getTime() - new Date(a.metadata.date).getTime());
+}
+
+export async function renderMarkdown(markdown: string): Promise<string> {
+  return marked(markdown);
+}
```

### `package.json`

```diff
@@ -16,7 +16,9 @@
     "clsx": "^2.1.1",
     "date-fns": "^4.1.0",
     "geist": "^1.7.0",
+    "gray-matter": "^4.0.3",
     "lucide-react": "^1.8.0",
+    "marked": "^18.0.10",
     "motion": "^12.39.0",
     "next": "16.1.7",
     "radix-ui": "^1.4.3",
```

### `pnpm-lock.yaml`

```diff
@@ -20,9 +20,15 @@ importers:
       geist:
         specifier: ^1.7.0
         version: 1.7.0(next@16.1.7(@babel/core@7.29.0)(react-dom@19.2.5(react@19.2.5))(react@19.2.5))
+      gray-matter:
+        specifier: ^4.0.3
+        version: 4.0.3
       lucide-react:
         specifier: ^1.8.0
         version: 1.8.0(react@19.2.5)
+      marked:
+        specifier: ^18.0.10
+        version: 18.0.10
       motion:
         specifier: ^12.39.0
         version: 12.39.0(react-dom@19.2.5(react@19.2.5))(react@19.2.5)
@@ -1637,6 +1643,9 @@ packages:
     resolution: {integrity: sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==}
     engines: {node: '>=8'}
 
+  argparse@1.0.10:
+    resolution: {integrity: sha512-o5Roy6tNG4SL/FOkCAN6RzjiakZS25RLYFrcMttJqbdd8BWrnA+fGz57iN5Pb06pvBGvl5gQ0B48dJlslXvoTg==}
+
   argparse@2.0.1:
     resolution: {integrity: sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==}
 
@@ -2198,6 +2207,10 @@ packages:
     resolution: {integrity: sha512-hIS4idWWai69NezIdRt2xFVofaF4j+6INOpJlVOLDO8zXGpUVEVzIYk12UUi2JzjEzWL3IOAxcTubgz9Po0yXw==}
     engines: {node: '>= 18'}
 
+  extend-shallow@2.0.1:
+    resolution: {integrity: sha512-zCnTtlxNoAiDc3gqY2aYAWFx7XWWiasuF2K8Me5WbN8otHKTUKBwjPtNpRs/rbUZm7KxWAaNj7P1a/p52GbVug==}
+    engines: {node: '>=0.10.0'}
+
   fast-deep-equal@3.1.3:
     resolution: {integrity: sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==}
 
@@ -2391,6 +2404,10 @@ packages:
     resolution: {integrity: sha512-5bJ+nf/UCpAjHM8i06fl7eLyVC9iuNAjm9qzkiu2ZGhM0VscSvS6WDPfAwkdkBuoXGM9FJSbKl6wylMwP9Ktig==}
     engines: {node: ^12.22.0 || ^14.16.0 || ^16.0.0 || >=17.0.0}
 
+  gray-matter@4.0.3:
+    resolution: {integrity: sha512-5v6yZd4JK3eMI3FqqCouswVqwugaA9r4dNZB1wwcmrD02QkV5H0y7XBQW8QwQqEaZY1pM9aqORSORhJRdNK44Q==}
+    engines: {node: '>=6.0'}
+
   has-bigints@1.1.0:
     resolution: {integrity: sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==}
     engines: {node: '>= 0.4'}
@@ -2525,6 +2542,10 @@ packages:
     engines: {node: ^12.20.0 || ^14.13.1 || >=16.0.0}
     hasBin: true
 
+  is-extendable@0.1.1:
+    resolution: {integrity: sha512-5BMULNob1vgFX6EjQw5izWDxrecWK9AM72rugNr0TFldMOi0fj6Jk+zeKIt0xGj4cEfQIJth4w3OKWOJ4f+AFw==}
+    engines: {node: '>=0.10.0'}
+
   is-extglob@2.1.1:
     resolution: {integrity: sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==}
     engines: {node: '>=0.10.0'}
@@ -2672,6 +2693,10 @@ packages:
   js-tokens@4.0.0:
     resolution: {integrity: sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==}
 
+  js-yaml@3.15.1:
+    resolution: {integrity: sha512-S99WuO3HlhO3XN41EtYUNl9zzXjoJx7QvmipxsJVxtCBT0YHEFy+iOJhjSvrmV12nYhWpZaM8lPHkJm0yUMbag==}
+    hasBin: true
+
   js-yaml@4.1.1:
     resolution: {integrity: sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==}
     hasBin: true
@@ -2718,6 +2743,10 @@ packages:
   keyv@4.5.4:
     resolution: {integrity: sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==}
 
+  kind-of@6.0.3:
+    resolution: {integrity: sha512-dcS1ul+9tmeD95T+x28/ehLgd9mENa3LsvDTtzm3vyBEO7RPptvAD+t44WVXaUjTBRcrpFeFlC8WCruUR456hw==}
+    engines: {node: '>=0.10.0'}
+
   kleur@3.0.3:
     resolution: {integrity: sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w==}
     engines: {node: '>=6'}
@@ -2836,6 +2865,11 @@ packages:
   magic-string@0.30.21:
     resolution: {integrity: sha512-vd2F4YUyEXKGcLHoq+TEyCjxueSeHnFxyyjNp80yg0XV4vUhnDer/lvvlqM/arB5bXQN5K2/3oinyCRyx8T2CQ==}
 
+  marked@18.0.10:
+    resolution: {integrity: sha512-FJeH4bRpYoXiggcgriCGItKCSv3xkngJc4QCZ/rkQCogU3VYaLxYJoZl8Nw/b4+x7iij/pd+09mZ6A1dXzpL0A==}
+    engines: {node: '>= 20'}
+    hasBin: true
+
   math-intrinsics@1.1.0:
     resolution: {integrity: sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==}
     engines: {node: '>= 0.4'}
@@ -3371,6 +3405,10 @@ packages:
   scheduler@0.27.0:
     resolution: {integrity: sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q==}
 
+  section-matter@1.0.0:
+    resolution: {integrity: sha512-vfD3pmTzGpufjScBh50YHKzEu2lxBWhVEHsNGoEXmCmn2hKGfeNLYMzCJpe8cD7gqX7TJluOVpBkAequ6dgMmA==}
+    engines: {node: '>=4'}
+
   semver@6.3.1:
     resolution: {integrity: sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==}
     hasBin: true
@@ -3453,6 +3491,9 @@ packages:
     resolution: {integrity: sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==}
     engines: {node: '>=0.10.0'}
 
+  sprintf-js@1.0.3:
+    resolution: {integrity: sha512-D9cPgkvLlV3t3IzL0D0YLvGA9Ahk4PcvVwUbN0dSGr1aP0Nrt4AEnTUbuGvquEC0mA64Gqt1fzirlRs5ibXx8g==}
+
   stable-hash@0.0.5:
     resolution: {integrity: sha512-+L3ccpzibovGXFK+Ap/f8LOS0ahMrHTf3xu7mMLSpEGU0EO9ucaysSylKo9eRDFNhWve/y275iPmIZ4z39a9iA==}
 
@@ -3514,6 +3555,10 @@ packages:
     resolution: {integrity: sha512-yDPMNjp4WyfYBkHnjIRLfca1i6KMyGCtsVgoKe/z1+6vukgaENdgGBZt+ZmKPc4gavvEZ5OgHfHdrazhgNyG7w==}
     engines: {node: '>=12'}
 
+  strip-bom-string@1.0.0:
+    resolution: {integrity: sha512-uCC2VHvQRYu+lMh4My/sFNmF2klFymLX1wHJeXnbEJERpV/ZsVuonzerjfrGpIGF7LBVa1O7i9kjiWvJiFck8g==}
+    engines: {node: '>=0.10.0'}
+
   strip-bom@3.0.0:
     resolution: {integrity: sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==}
     engines: {node: '>=4'}
@@ -5412,6 +5457,10 @@ snapshots:
     dependencies:
       color-convert: 2.0.1
 
+  argparse@1.0.10:
+    dependencies:
+      sprintf-js: 1.0.3
+
   argparse@2.0.1: {}
 
   aria-hidden@1.2.6:
@@ -6146,6 +6195,10 @@ snapshots:
     transitivePeerDependencies:
       - supports-color
 
+  extend-shallow@2.0.1:
+    dependencies:
+      is-extendable: 0.1.1
+
   fast-deep-equal@3.1.3: {}
 
   fast-glob@3.3.1:
@@ -6334,6 +6387,13 @@ snapshots:
 
   graphql@16.13.2: {}
 
+  gray-matter@4.0.3:
+    dependencies:
+      js-yaml: 3.15.1
+      kind-of: 6.0.3
+      section-matter: 1.0.0
+      strip-bom-string: 1.0.0
+
   has-bigints@1.1.0: {}
 
   has-flag@4.0.0: {}
@@ -6460,6 +6520,8 @@ snapshots:
 
   is-docker@3.0.0: {}
 
+  is-extendable@0.1.1: {}
+
   is-extglob@2.1.1: {}
 
   is-finalizationregistry@1.1.1:
@@ -6581,6 +6643,11 @@ snapshots:
 
   js-tokens@4.0.0: {}
 
+  js-yaml@3.15.1:
+    dependencies:
+      argparse: 1.0.10
+      esprima: 4.0.1
+
   js-yaml@4.1.1:
     dependencies:
       argparse: 2.0.1
@@ -6622,6 +6689,8 @@ snapshots:
     dependencies:
       json-buffer: 3.0.1
 
+  kind-of@6.0.3: {}
+
   kleur@3.0.3: {}
 
   kleur@4.1.5: {}
@@ -6715,6 +6784,8 @@ snapshots:
     dependencies:
       '@jridgewell/sourcemap-codec': 1.5.5
 
+  marked@18.0.10: {}
+
   math-intrinsics@1.1.0: {}
 
   media-typer@1.1.0: {}
@@ -7260,6 +7331,11 @@ snapshots:
 
   scheduler@0.27.0: {}
 
+  section-matter@1.0.0:
+    dependencies:
+      extend-shallow: 2.0.1
+      kind-of: 6.0.3
+
   semver@6.3.1: {}
 
   semver@7.7.4: {}
@@ -7432,6 +7508,8 @@ snapshots:
 
   source-map@0.6.1: {}
 
+  sprintf-js@1.0.3: {}
+
   stable-hash@0.0.5: {}
 
   statuses@2.0.2: {}
@@ -7521,6 +7599,8 @@ snapshots:
     dependencies:
       ansi-regex: 6.2.2
 
+  strip-bom-string@1.0.0: {}
+
   strip-bom@3.0.0: {}
 
   strip-final-newline@2.0.0: {}
```

### `public/blogs/building-scalable-frontends.md`

```diff
@@ -0,0 +1,124 @@
+---
+title: Building Scalable Frontend Systems
+description: A deep dive into architectural patterns and best practices for building frontend systems that scale.
+date: 2026-08-15
+author: Manish Bisht
+reading_time: 8
+---
+
+# Building Scalable Frontend Systems
+
+When you start a new frontend project, everything feels simple. A few components here, some state management there, and you're done. But as your application grows, complexity compounds. Features pile up, components become interdependent, and suddenly adding a single button feels like moving a mountain.
+
+The question isn't whether your frontend will need to scale—it's whether you'll be ready when it does.
+
+## The Architecture Problem
+
+I've seen many teams approach scaling reactively. They write code that works, ship features, and when performance or maintainability becomes an issue, they scramble to refactor. This is expensive, error-prone, and demoralizing.
+
+The better approach? Think about scalability from day one.
+
+### Component Organization
+
+Your first instinct might be to organize by file type:
+
+```
+components/
+  buttons/
+  inputs/
+  modals/
+  ...
+```
+
+This approach works for small projects but becomes a nightmare at scale. When you need to change a component, you're hunting across multiple directories.
+
+Instead, organize by feature:
+
+```
+components/
+  auth/
+    LoginForm.tsx
+    RegisterForm.tsx
+    PasswordReset.tsx
+  dashboard/
+    Dashboard.tsx
+    Charts.tsx
+    Widgets.tsx
+  shared/
+    Button.tsx
+    Input.tsx
+    Card.tsx
+```
+
+This structure makes it clear which components belong together and easier to maintain related functionality.
+
+## State Management Strategy
+
+The state management landscape is crowded. Redux, Zustand, Jotai, Recoil—each has merits. But the real question isn't which tool to use; it's *when* you need centralized state at all.
+
+**Local state first.** Keep state as close to where it's used as possible. `useState` for a form? Perfect. A modal's open state? Great.
+
+**Component communication through props.** If you have a few levels of nesting, prop drilling isn't that painful, and it makes data flow explicit.
+
+**Global state when necessary.** Only reach for a state management library when multiple unrelated parts of your app need the same data, or when performance requires it.
+
+## Performance Optimization
+
+Scalability isn't just about code organization—it's about how your app performs as it grows.
+
+### Code Splitting
+
+Load only what you need:
+
+```tsx
+import dynamic from 'next/dynamic';
+
+const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
+  loading: () => <Skeleton />,
+});
+```
+
+### Memoization (Use Carefully)
+
+Premature optimization is the root of all evil. Only memoize when you've measured and found a bottleneck.
+
+```tsx
+const ExpensiveComponent = memo(({ data }) => {
+  return <div>{/* render something expensive */}</div>;
+});
+```
+
+### Virtual Scrolling for Large Lists
+
+When you have hundreds of items, render only the visible ones:
+
+```tsx
+<VirtualList items={items} renderItem={renderRow} />
+```
+
+## Testing at Scale
+
+As your codebase grows, tests become your safety net. But testing everything is impossible.
+
+Focus your testing efforts:
+
+1. **Unit tests** for pure functions and utilities
+2. **Integration tests** for component interactions
+3. **E2E tests** for critical user flows
+
+Write the test that would have caught each bug you've shipped. Over time, you'll build confidence in your ability to refactor safely.
+
+## Monitoring and Observability
+
+You can't improve what you don't measure.
+
+- **Web Vitals:** Use tools like web-vitals to track Core Web Vitals
+- **Error tracking:** Integrate Sentry or similar to catch production errors
+- **Analytics:** Understand how users actually use your app
+- **Performance profiling:** Regularly profile your app to find bottlenecks
+
+## Conclusion
+
+Building scalable frontends isn't about being perfect from day one. It's about making deliberate choices that leave room for growth, making it easy to maintain as complexity increases, and measuring to know when to optimize.
+
+Start simple, think ahead, measure often, and refactor when needed. Your future self will thank you.
```

### `utils/date.ts`

```diff
@@ -1,4 +1,4 @@
-import { intervalToDuration } from 'date-fns';
+import { intervalToDuration, format } from 'date-fns';
 
 function parseMonthYear(input: string) {
   const [month, year] = input.split('/').map(Number);
@@ -16,3 +16,12 @@ export function getDuration(startDate: string, endDate?: string) {
   if (months) return `${months}m`;
   return '0m';
 }
+
+export function formatDate(dateString: string): string {
+  try {
+    const date = new Date(dateString);
+    return format(date, 'MMM d, yyyy');
+  } catch {
+    return dateString;
+  }
+}
```

---

## ManishBisht777/Arceus

### Commit `2b87aa6deeb516cb64108189d1fe4b156ccf331c`

**Message:** Update README by removing license section

Removed license section and cleaned up author information.

### `README.md`

```diff
@@ -407,13 +407,9 @@ To extend or modify Arceus:
 - Check GH_TOKEN is valid and has repo permissions
 - Ensure ARCEUS_PROD_BRANCH exists on remote
 
-## 📄 License
-
-[Specify your project's license]
-
 ## 👤 Author
 
-Manish Bisht (manish@delightree.com)
+Manish Bisht
 
 ---
 
```

---

